# Data Ingestion Engineering — Nguyễn Trung Duy

Bài cá nhân **2A202603387 — L3A**. Chương trình đọc PDF, chia đoạn, tạo embedding thật, lưu PostgreSQL + pgvector và tìm 3 đoạn liên quan đến câu hỏi. Kết quả được so sánh giữa ba cấu hình A/B/C.

## Kết quả hiện tại

| Cấu hình | Số chunk | Dev Hit@1 | Dev Hit@3 | Test Hit@1 | Test Hit@3 |
|---|---:|---:|---:|---:|---:|
| A | 151 | 3/15 | 7/15 | 4/5 | 4/5 |
| B | 104 | 3/15 | 10/15 | 3/5 | 4/5 |
| C | 104, dùng lại B | 3/15 | 10/15 | 3/5 | 4/5 |

B được chọn trên dev trước khi chạy test. Khi B/C bằng điểm và số chunk thì chọn theo thứ tự tên cấu hình, đúng quy tắc đã ghi.

Xem [báo cáo cá nhân](report/individual/2A202603387_NguyenTrungDuy.md), [nhật ký thí nghiệm](artifacts/experiment_log.csv) và [kết quả đầy đủ](starter/results/).

## Dữ liệu và giấy phép

Dùng **Think Python: How to Think Like a Computer Scientist**, Allen B. Downey, 2nd Edition, Version 2.4.1, Green Tea Press. PDF gốc có 244 trang; chỉ nạp **trang vật lý 111–146**, gồm chương Lists, Dictionaries và Tuples. Có 36 trang nội dung, tổng 60.820 ký tự sau chuẩn hóa NFC.

- [PDF chính thức](https://greenteapress.com/thinkpython2/thinkpython2.pdf).
- File local: `starter/data/thinkpython2.pdf`.
- Giấy phép tại trang vật lý 4: **CC BY-NC 3.0 Unported**. Copyright © 2015 Allen Downey. Giữ thông tin tác giả/nguồn và dùng phi thương mại; giữ ghi nguồn của nội dung bên thứ ba được dẫn trong sách.
- [Manifest](data/manifest.json): quyền sử dụng, nguồn, snapshot SHA-256, danh sách trang, cách tính và số ký tự từng trang.

PDF không chỉnh sửa. Bản text trích xuất được chuẩn hóa Unicode NFC, giữ xuống dòng và chia chunk. Thời điểm kiểm tra snapshot được ghi trong manifest; ngày tải lần đầu không được thu lại.

## Pipeline và ba cấu hình

```text
thinkpython2.pdf
  → read_pdf.py → pages.json
  → chunk_pages.py / chunk_sections.py → chunks_A.json / chunks_B.json
  → embed_chunks.py → chunks_A_embedded.json / chunks_B_embedded.json
  → load_database.py → PostgreSQL + pgvector
  → search.py → câu hỏi → embedding → top-3
  → evaluate_dev.py → chọn cấu hình → evaluate_test.py
```

| Cấu hình | Cách chia | Tìm kiếm |
|---|---|---|
| A | 500 ký tự, overlap 50 | Không lọc |
| B | Theo tiêu đề mục; phần dài chia tối đa 1.000 ký tự; giữ ranh giới trang | Không lọc |
| C | Dùng đúng chunk và embedding của B | Lọc chapter khi câu hỏi cung cấp |

C không tạo thêm bộ embedding. Câu không có filter thì C tìm giống B. Metadata mỗi chunk gồm `document_id`, `source`, `page`, `chapter`.

Model local: `sentence-transformers/all-MiniLM-L6-v2`, **384 chiều**, chuẩn hóa vector document/query. PostgreSQL dùng cosine distance (`<=>`) và trả top-3. Hiện chưa có vector index approximate nên dùng exact search.

## 1. Cài môi trường

Đã chạy trên Windows, **Python 3.12.10**, Docker Desktop và WSL 2. Lần đầu cần mạng để tải thư viện, model và Docker image.

Từ thư mục gốc repo, mở PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r starter/requirements.txt
cd starter
```

Không cần kích hoạt `.venv` nếu dùng đường dẫn Python như hướng dẫn. Nếu đã kích hoạt `(.venv)` thì có thể thay `..\.venv\Scripts\python.exe` bằng `python`.

`requirements.txt` dùng pg8000, không cần psycopg hay Chroma. Các phiên bản được ghi từ môi trường đang hoạt động; đây không phải lockfile cho toàn bộ dependency gián tiếp.

## 2. Khởi động database

Mở Docker Desktop. Các lệnh sau chạy từ **`starter/`**:

```powershell
docker compose -p day6_student_starter up -d --wait
docker compose -p day6_student_starter ps
Get-Content -Raw create_tables.sql | docker compose -p day6_student_starter exec -T postgres psql -U day6 -d day6_lab -v ON_ERROR_STOP=1
..\.venv\Scripts\python.exe check_database.py
```

Database: `day6_lab`, user `day6`, cổng `127.0.0.1:55433`. Mật khẩu local của bài thực hành nằm trong `docker-compose.yml` và các script kết nối. Chỉ dùng cấu hình này cho lab trên máy.

Dữ liệu database nằm trong Docker volume. Dừng nhưng giữ dữ liệu:

```powershell
docker compose -p day6_student_starter stop
```

## 3. Đọc tài liệu, tạo chunk và embedding

```powershell
..\.venv\Scripts\python.exe read_pdf.py
..\.venv\Scripts\python.exe chunk_pages.py
..\.venv\Scripts\python.exe chunk_sections.py
..\.venv\Scripts\python.exe embed_chunks.py
..\.venv\Scripts\python.exe check_embeddings.py
..\.venv\Scripts\python.exe load_database.py
..\.venv\Scripts\python.exe create_manifest.py
```

Nếu dùng các file embedding đã có trong repo, có thể chỉ chạy `check_embeddings.py` rồi `load_database.py` để nạp vào database mới. Lệnh nạp upsert theo `(strategy, chunk_id)`, kiểm tra 384 chiều, xóa chunk cũ của đúng tài liệu/cấu hình và dùng transaction. Chạy lại không tạo dòng trùng.

Kết quả mong đợi: 36 trang, 151 chunk A, 104 chunk B, mỗi vector 384 chiều.

## 4. Thử tìm kiếm

```powershell
..\.venv\Scripts\python.exe search.py
```

Nhập một câu tiếng Anh khi được hỏi, hoặc dùng:

```powershell
..\.venv\Scripts\python.exe search.py --strategy A --question "How do I remove an item from a list?"
..\.venv\Scripts\python.exe search.py --strategy B --question "How do I remove an item from a list?"
..\.venv\Scripts\python.exe search.py --strategy C --chapter 10 --question "How do I remove an item from a list?"
```

Kết quả là 3 đoạn kèm nguồn, trang, chương và điểm cosine. Chương là điều kiện người dùng cung cấp, không được suy từ gold. Chương trình tìm bằng chứng, chưa sinh câu trả lời kiểu chatbot.

## 5. Benchmark và đánh giá

[benchmark/questions.json](benchmark/questions.json) có 20 câu: Q01–Q15 dev, Q16–Q20 test. Mỗi câu có đáp án và bằng chứng. Q03, Q09, Q14, Q19 có filter chương; Q19 thuộc test.

Kết quả hiện tại đã chạy và nằm trong `starter/results/`. Để xem báo cáo, không cần chạy lại.

Nếu tạo một thí nghiệm mới trên bản sao repo, giữ riêng bộ kết quả hiện tại và bắt đầu với thư mục `starter/results/` không chứa các kết quả đã chốt. Không dùng test đã xem để tinh chỉnh rồi coi là holdout mới. Thứ tự chạy:

```powershell
..\.venv\Scripts\python.exe evaluate_dev.py
..\.venv\Scripts\python.exe evaluate_test.py
```

- Dev chạy cùng 15 câu cho A/B/C.
- Test script ghi lựa chọn từ dev và khóa hash các file trước khi tìm 5 câu test.
- Test script từ chối ghi đè khi đã có kết quả test.
- Một hit phải đúng nguồn/trang và chứa trọn quote trong một chunk, sau chuẩn hóa Unicode/khoảng trắng. Nhãn grounding/coherence được lưu riêng với metric hit.

Các file đánh giá:

| Nội dung | File trong `starter/results/` |
|---|---|
| Điểm dev/test | `dev_metrics.json`, `test_metrics.json` |
| Top-3 đầy đủ, gold và nhãn hit | `dev_traces.json`, `test_traces.json` |
| Lựa chọn B trước test | `selection.json` |
| Coherence: mẫu, điểm và lý do | `coherence_audit.json`, `coherence_review.md`, `coherence_summary.json` |
| Metadata/grounding | `test_audit.json`, `test_review.md`, `test_audit_summary.json` |
| Tài nguyên và giới hạn token | `resource_summary.json` |

`prepare_coherence_review.py` và `prepare_test_review.py` tạo mẫu trên một thí nghiệm mới. Hiện đã có các file nhãn; không cần chạy lại các lệnh chuẩn bị mẫu để đọc kết quả.

## Kiểm thử và phép đo bổ sung

Các kiểm tra sau dùng thư mục tạm và schema PostgreSQL riêng. Chúng không thay `public.chunks` hoặc các kết quả dev/test đã chốt:

```powershell
# Chạy từ starter/, sau khi Docker và database đã sẵn sàng
..\.venv\Scripts\python.exe verify_pipeline.py
```

Script kiểm tra lại pipeline đọc/chia đoạn, vector 384 chiều, nạp lặp không trùng, thay text/vector khi tài liệu đổi, xóa chunk cũ, hoàn tác khi có lỗi SQL, cosine và filter. Đồng thời đo thời gian xử lý thật. Kết quả trong `results/supplementary_verification.json` và bản đọc `results/supplementary_verification.md`.

`model_snapshot.json` ghi revision cố định và SHA-256 các file model. Việc tái tạo vector bằng revision này được đối chiếu với vector cũ theo dung sai số học, không sửa lại thông tin lịch sử của lần dev/test.

Chuẩn bị chunk không vượt giới hạn token cho một thí nghiệm sau:

```powershell
..\.venv\Scripts\python.exe build_token_safe_chunks.py
```

Đầu ra ở `results/token_safe/`: A có 151 chunk, B có 134 chunk, tất cả không vượt 256 token và giữ đủ ký tự từ chunk gốc. C sẽ dùng chung B. Các chunk mới **chưa được tạo embedding, nạp database hoặc chạy benchmark**; không dùng kết quả test cũ làm điểm cho bộ mới.

## Giới hạn cần đọc trước khi diễn giải kết quả

- Model giới hạn 256 token. Kiểm tra sau test phát hiện **30/104 chunk B/C** vượt giới hạn; phần text cuối không tham gia embedding dù vẫn được lưu trong database. Không sửa kết quả thí nghiệm hiện tại để che hạn chế này.
- Lần dev/test ban đầu chưa ghi revision. Phép kiểm tra bổ sung đã cố định snapshot trong `starter/model_snapshot.json` và đối chiếu vector tái tạo với file gốc.
- A–B thay đồng thời cách chia, kích thước và overlap; chỉ B–C là so sánh thay đúng một yếu tố filter.
- Test chỉ có 5 câu và một câu filter. Mẫu coherence chỉ lấy 10 trang đầu của chương Lists.
- Thời gian truy xuất có trong trace. Đọc PDF, document embedding và ingest đã được đo trong một lượt kiểm chứng bổ sung, lưu riêng với lần chạy ban đầu. RAM cực đại, điện và phần cứng chưa đo; phí API 0 USD.
- PDF có lỗi dính chữ/sơ đồ bị trải phẳng. Sách năm 2015 chứa một số mô tả Python cũ, ví dụ thứ tự dictionary.

## File nào là phần triển khai thực tế?

Các script ngay dưới `starter/` là pipeline đang sử dụng. Thư mục `starter/src/` và `starter/scripts/check_setup.py` là khung/tham khảo từ đề bài; pipeline hiện tại dùng `check_database.py` và pg8000. Không chạy `python -m src.run` để thay cho các lệnh trong README này.
