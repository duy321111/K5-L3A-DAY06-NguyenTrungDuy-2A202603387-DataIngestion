# Báo cáo cá nhân — Data Ingestion Engineering

- Học viên: Nguyễn Trung Duy.
- MSSV: 2A202603387. Lớp: L3A.
- Chủ đề: tìm kiếm kiến thức List, Dictionary và Tuple trong Think Python.
- Repo: https://github.com/duy321111/K5-L3A-DAY06-NguyenTrungDuy-2A202603387-DataIngestion

## 1. Dữ liệu và pipeline

### Dữ liệu

Dữ liệu lấy từ sách **Think Python: How to Think Like a Computer Scientist**, Allen B. Downey, 2nd Edition, Version 2.4.1, Green Tea Press. File gốc có 244 trang. Bài này chỉ dùng trang vật lý PDF **111–146**, tương ứng trang in 89–124, gồm chương 10 Lists, chương 11 Dictionaries và chương 12 Tuples.

Nguồn: https://greenteapress.com/thinkpython2/thinkpython2.pdf. Trang vật lý 4 ghi giấy phép **CC BY-NC 3.0 Unported**. Khi chia sẻ cần giữ thông tin tác giả, nguồn và dùng phi thương mại; các nội dung được dẫn từ bên thứ ba vẫn cần giữ ghi nguồn tương ứng.

Có **36 trang nội dung**, tổng **60,820 ký tự** sau chuẩn hóa NFC, gồm cả khoảng trắng và xuống dòng. Các trang này có giải thích, ví dụ, thuật ngữ và bài tập; không lấy bìa, mục lục hay phần tài liệu tham khảo ngoài khoảng đã chọn. Trang ngắn vẫn được tính theo trang PDF thực, không nhân bản để đủ số lượng.

Manifest: [data/manifest.json](../../data/manifest.json). File có danh sách page ID, chương, số ký tự từng trang, nguồn, giấy phép và SHA-256 của snapshot. Trường accessed_at là lúc kiểm tra bản local để lập manifest; thời điểm tải file đầu tiên không được ghi lại.

### Luồng xử lý

PDF → đọc chữ từng trang → chuẩn hóa Unicode NFC → chia chunk A/B → tạo embedding → lưu PostgreSQL + pgvector → tạo embedding câu hỏi → truy xuất top-3 → đánh giá dev/test.

| Bước | File thực hiện | Đầu ra |
|---|---|---|
| Đọc và chuẩn hóa | `starter/read_pdf.py` | `starter/data/pages.json` |
| Chia cố định | `starter/chunk_pages.py` | `chunks_A.json` |
| Chia theo mục | `starter/chunk_sections.py` | `chunks_B.json` |
| Tạo embedding | `starter/embed_chunks.py` | `chunks_A_embedded.json`, `chunks_B_embedded.json` |
| Tạo bảng/nạp dữ liệu | `starter/create_tables.sql`, `starter/load_database.py` | Bảng `chunks` |
| Tìm kiếm | `starter/search.py` | Top-3 kèm score và metadata |
| Đánh giá | `starter/evaluate_dev.py`, `starter/evaluate_test.py` | Trace và chỉ số theo split |

Không dùng OCR vì cả 36 trang đều lấy được chữ. Văn bản giữ xuống dòng để nhận diện tiêu đề; không tự sửa các lỗi dính tên hàm với chữ bên cạnh. Các sơ đồ có thể bị trải thành chữ/số rời. Trang không lấy được chữ được gắn trạng thái empty; dữ liệu hiện tại có 36 trang ok.

### Model, database và metadata

- Embedding: `sentence-transformers/all-MiniLM-L6-v2`, chạy local, 384 chiều; document và query cùng dùng `normalize_embeddings=True`.
- Giới hạn model ghi trong lần chạy: **256 token**. Chưa pin revision model; `resolved_model_revision` trong test_run.json là null. Đây là một giới hạn tái lập, không tự điền revision chưa xác minh.
- Database đang kiểm tra: PostgreSQL 16.16 (Debian 16.16-1.pgdg12+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 12.2.0-14+deb12u1) 12.2.0, 64-bit. pgvector: 0.8.7.
- Metric: cosine distance, SQL dùng toán tử `<=>`, sắp xếp tăng dần và `LIMIT 3`; score hiển thị bằng `1 - distance`. Bảng hiện chỉ có khóa chính B-tree, chưa có HNSW/IVFFlat nên truy xuất là exact search.
- Driver kết nối: pg8000. Chroma và psycopg từng bị Windows chặn DLL; pipeline thực tế dùng PostgreSQL trong Docker và pg8000 viết bằng Python.
- Metadata gồm `document_id`, `source`, `page`, `chapter`. Số trang là vị trí vật lý trong PDF. Chương 10 áp dụng trang 111–124, chương 11 trang 125–136, chương 12 trang 137–146, đối chiếu từ tiêu đề sách.
- Chunk có ID ổn định theo vị trí. Nạp bằng upsert; cùng khóa `(strategy, chunk_id)` thì cập nhật. Xóa các ID cũ không còn trong JSON của đúng tài liệu/cấu hình, thực hiện trong transaction để tránh nạp dở.

Phiên bản môi trường được ghi khi lập báo cáo, không phải log phiên bản đã thu ngay lúc ingest:

| Thành phần | Phiên bản |
|---|---|
| python | 3.12.10 |
| pypdf | 7.0.1 |
| fonttools | 4.68.0 |
| sentence-transformers | 6.3.0 |
| torch | 2.15.0 |
| pg8000 | 1.31.6 |

## 2. Cấu hình và benchmark

| Cấu hình | Cách chia | Overlap | Lọc khi truy xuất |
|---|---|---:|---|
| A | Cố định 500 ký tự, không nối qua trang | 50 ký tự | Không |
| B | Theo tiêu đề mục; phần dài chia tối đa 1.000 ký tự; giữ ranh giới trang | 0 | Không |
| C | Dùng nguyên chunk và embedding của B | 0 | Theo chapter nếu câu hỏi cung cấp |

A–B đồng thời thay cách chia, giới hạn độ dài và overlap, nên kết quả chỉ phản ánh tác động chung của cấu hình chunking. B–C chỉ thay bộ lọc truy xuất, phù hợp để xem riêng ảnh hưởng filter. Không tạo thêm bộ embedding khác cho C.

Benchmark có **20 câu tiếng Anh**, lưu ở [benchmark/questions.json](../../benchmark/questions.json): Q01–Q15 là dev, Q16–Q20 là test. Mỗi câu có đáp án, nguồn, số trang và đoạn bằng chứng. Các quote đã được kiểm tra tồn tại sau chuẩn hóa khoảng trắng. Dev/test dùng cùng sách nên vẫn có tương đồng chủ đề.

Các câu có filter là **Q03, Q09, Q14 và Q19**, trong đó Q19 thuộc test. Filter chương được ghi ngay trong nội dung câu hỏi. Chỉ câu hỏi được dùng để tạo query vector; đáp án, trang gold và quote chỉ dùng đối chiếu sau tìm kiếm. Không suy filter từ gold.

Quy tắc chọn được ghi trong experiment_config.json: ưu tiên dev Evidence Hit@3, sau đó dev Hit@1, rồi ít chunk hơn, cuối cùng tên cấu hình theo thứ tự chữ cái.

**Cấu hình đã chọn: B.** Lựa chọn được lưu lúc 13/11/2026 22:54:37 và test hoàn tất lúc 13/11/2026 22:55:02 (giờ Việt Nam). B/C bằng điểm dev và cùng số chunk nên B được chọn theo quy tắc cuối. Kết quả test không được dùng để chọn lại.

Config, benchmark, PDF, code tìm kiếm và các file embedding có SHA-256 tại thời điểm dev/chốt. evaluate_test.py kiểm tra các hash và vector trong database trước khi chạy; không ghi đè test nếu đã có kết quả.

## 3. Kết quả truy xuất

Một hit cần đúng nguồn/trang và chứa trọn bằng chứng trong một chunk sau chuẩn hóa NFC/khoảng trắng. Quote bị tách qua hai chunk không đạt định nghĩa chính. Cách so khớp tự động này nghiêm ngặt và có thể bỏ sót bằng chứng tương đương chưa được khai báo.

| Cấu hình | Split | Hit@1 | Evidence Hit@3 | Số chunk | Trung bình tìm kiếm (ms/câu) | Phí API (USD) |
|---|---|---:|---:|---:|---:|---:|
| A | dev | 3/15 | 7/15 | 151 | 99.58 | 0 |
| B | dev | 3/15 | 10/15 | 104 | 102.43 | 0 |
| C | dev | 3/15 | 10/15 | 104 | 93.08 | 0 |
| A | test | 4/5 | 4/5 | 151 | 131.49 | 0 |
| B | test | 3/5 | 4/5 | 104 | 102.21 | 0 |
| C | test | 3/5 | 4/5 | 104 | 91.97 | 0 |

Trace đầy đủ nằm tại [dev_traces.json](../../starter/results/dev_traces.json) và [test_traces.json](../../starter/results/test_traces.json); bảng điểm tại dev_metrics.json và test_metrics.json. Tổng cộng 45 lượt dev và 15 lượt test, mỗi lượt lưu đủ 3 kết quả cùng ID, nội dung, score, metadata, gold và nhãn hit.

## 4. Coherence, metadata và grounding

### Cách đánh giá

Coherence dùng cùng 10 trang đầu theo thứ tự 111–120. Trên mỗi trang chọn ký tự không trắng đầu tiên từ giữa trang trở đi; nếu nhiều chunk bao phủ thì lấy chunk bắt đầu sớm nhất. Quy tắc lấy mẫu được xác định trước khi chấm coherence, không dựa vào kết quả tốt/xấu của từng chunk. C dùng đúng chunk của B.

Điểm coherence: 0 = thiếu ngữ cảnh đến mức không hiểu; 1 = hiểu một phần nhưng thiếu ý; 2 = có thể đọc độc lập và giữ trọn ý. Mỗi mẫu có đoạn nguồn, chunk, điểm và lý do tại [coherence_audit.json](../../starter/results/coherence_audit.json), bản đọc tại coherence_review.md.

Metadata và grounding dùng cùng 5 câu test cho A/B/C. Mỗi cấu hình kiểm tra 15 bản ghi top-3 về nguồn/trang/chương, đối chiếu PDF. Grounding chấm chung ba kết quả: 0 = không có bằng chứng, 1 = có nhưng chưa đủ, 2 = đủ trả lời và truy nguồn. Đây là chất lượng bằng chứng truy xuất, không phải độ chính xác câu trả lời LLM.

Nhãn và lý do được lưu tại [test_audit.json](../../starter/results/test_audit.json), bản đọc tại test_review.md. Không suy điểm coherence/grounding trực tiếp từ Hit@3. Các đánh giá chưa có kiểm chứng độc lập giữa nhiều người, có nguy cơ thiên lệch; không dùng tên học viên được giao rà soát làm bằng chứng rằng học viên đã tự chấm.

| Cấu hình | Coherence /2 (10 mẫu) | Metadata đúng | Top-3 đúng chương ở câu filter | Grounding 0/1/2 | Grounding /2 (5 câu) |
|---|---:|---:|---:|---|---:|
| A | 1.0 | 15/15 | 1/1 | 1 / 0 / 4 | 1.6 |
| B | 1.5 | 15/15 | 1/1 | 1 / 0 / 4 | 1.6 |
| C | 1.5 | 15/15 | 1/1 | 1 / 0 / 4 | 1.6 |

B/C có 5 mẫu coherence mức 2 và 5 mẫu mức 1; A có 10 mẫu mức 1. Các đoạn A thường bị cắt đầu/cuối từ hoặc câu. B vẫn có thể bị cắt do giới hạn 1.000 ký tự. Mẫu coherence đều thuộc chương Lists, chưa đại diện cho toàn bộ corpus.

`source` và `page` giúp mở lại đúng tài liệu/trang để xác minh. `chapter` giúp thu hẹp phạm vi khi người dùng yêu cầu chương. Metadata đúng không bảo đảm đoạn liên quan: A_Q18 có metadata đúng nhưng không chứa giải thích về toán tử in.

Q19 là câu test duy nhất có filter chapter=12. C thực sự lọc trong SQL; A/B không lọc nhưng lần chạy này cũng trả về top-3 thuộc chương 12. Vì vậy 1/1 ở A/B chỉ là tuân thủ phạm vi tình cờ trên mẫu này, không chứng minh A/B có tính năng lọc. Không thấy lỗi metadata trong 45 bản ghi đã đối chiếu.

## 5. Tác động chiến lược và tài nguyên

### So sánh A–B

B đạt dev Hit@3 10/15 so với A 7/15, tăng 3 câu. Coherence mẫu tăng từ 1,0 lên 1,5/2. Số chunk giảm từ 151 xuống 104, ít hơn 47 chunk (khoảng 31,1%). Tuy nhiên dev Hit@1 không đổi, đều 3/15. Trên test, Hit@3 bằng nhau 4/5 và A có Hit@1 cao hơn B (4/5 so với 3/5). Không có cơ sở nói B tốt hơn A ở mọi chỉ số.

### So sánh B–C

B/C cùng chunk, model và vector, chỉ khác filter. Điểm tổng dev/test bằng nhau. C có giá trị kiểm soát phạm vi khi người dùng cung cấp chương, nhưng benchmark hiện ít câu filter và các chương khá dễ phân biệt, nên chưa thấy cải thiện về số câu có bằng chứng. Không suy rộng rằng metadata filter không hữu ích trong dữ liệu khác.

### Tài nguyên

| Cấu hình lưu trữ | Số chunk | Tổng ký tự chunk | Độ dài nhỏ nhất / trung bình / lớn nhất | JSON có embedding (byte) |
|---|---:|---:|---|---:|
| A | 151 | 66570 | 70 / 440.86 / 500 | 1784441 |
| B | 104 | 60774 | 20 / 584.37 / 1000 | 1244667 |

C dùng lại dữ liệu B nên không cần một bộ vector mới. Kích thước JSON không phải kích thước toàn database. Tổng ký tự A lớn hơn nguồn vì overlap; B loại khoảng trắng đầu/cuối đoạn.

Thời gian tạo query embedding chung cho 15 câu dev là 0.138 giây; cho 5 câu test là 0.117 giây. Vector query được tạo một lần rồi dùng chung A/B/C.

Thời gian tìm kiếm trong bảng kết quả gồm mở kết nối PostgreSQL, truy vấn đếm và truy vấn top-3; không gồm tải model và tạo embedding. Chỉ có một lượt chạy tuần tự A → B → C, nên cache, thứ tự chạy và mở kết nối có thể ảnh hưởng. Không kết luận C nhanh hơn chỉ từ các số trung bình này.

Phí gọi API embedding là 0 USD vì model chạy local. Chưa đo chi phí điện/phần cứng. Thời gian đọc PDF, tạo document embedding, ingest và RAM cực đại không được thu ở lần chạy ban đầu, nên báo cáo không tự tạo số liệu cho các mục đó. Thống kê kiểm chứng ở [resource_summary.json](../../starter/results/resource_summary.json).

### Giới hạn token được phát hiện khi lập báo cáo

Model dùng giới hạn 256 token. A có 0/151 chunk vượt giới hạn, token lớn nhất 255. B/C có **30/104 chunk vượt giới hạn**, token lớn nhất 384.

Đây là hạn chế quan trọng: model.encode cắt phần vượt giới hạn trước khi tạo embedding, dù text đầy đủ vẫn được lưu để hiển thị và chấm evidence. Vì vậy thông tin ở cuối chunk B/C có thể không tham gia xếp hạng. Không thể quy mọi chênh lệch A–B cho ranh giới tiêu đề. Kiểm tra token được thực hiện sau test; không sửa chunk và chạy lại test để trình bày như holdout mới.

### Ví dụ thất bại

1. **A_Q18 — toán tử in trên dictionary.** Gold ở trang PDF 126. Top-3 lại thuộc trang 130, 125, 125, nói về hash và ánh xạ key/value nhưng không giải thích membership kiểm tra key. Hit@3 không đạt; grounding 0.
2. **B_Q16 và C_Q16 — list lồng có tính là một phần tử không.** Gold ở trang PDF 113. Top-3 có trang 113 nhưng là mục slice và phép toán list, cùng trang 141 về zip. Đúng trang không đồng nghĩa đúng bằng chứng; Hit@3 không đạt và grounding 0.
3. **A_p111 — coherence.** Chunk bắt đầu ở giữa câu và kết thúc bằng with em, cắt dở từ empty. Phần giữa vẫn hiểu được nên mức 1; B/C giữ trọn mục 10.1 ở vị trí này và được mức 2.

### Kết luận và hướng cải tiến

Giữ lựa chọn **B** theo quy tắc dev đã công bố. B có ít chunk hơn A và giữ ngữ cảnh tốt hơn trong mẫu coherence; C có thể dùng khi người dùng cung cấp filter. Đây là lựa chọn cho corpus và benchmark nhỏ của bài, không phải kết luận chiến lược tốt nhất tổng quát.

Nếu làm thí nghiệm tiếp theo: giới hạn chunk bằng token của model, cắt ở cuối câu để giảm dở ý, pin revision model, đo thời gian ingest ngay từ đầu, lấy mẫu coherence ở cả ba chương và mở rộng câu filter. Các thay đổi đó cần bộ test mới hoặc phải công bố rõ là thí nghiệm sau khi đã xem test.

## 6. Lệnh chạy và các file minh chứng

Từ thư mục gốc, sau khi cài môi trường Python và mở Docker Desktop:

```powershell
cd starter
docker compose -p day6_student_starter up -d --wait
Get-Content -Raw create_tables.sql | docker compose -p day6_student_starter exec -T postgres psql -U day6 -d day6_lab -v ON_ERROR_STOP=1
python read_pdf.py
python chunk_pages.py
python chunk_sections.py
python embed_chunks.py
python check_embeddings.py
python load_database.py
python check_database.py
python search.py --question "How do I remove an item from a list?"
```

Các lệnh trên mô tả cách tái tạo phần dữ liệu/tìm kiếm; không cần chạy lại để đọc báo cáo. Kết quả dev/test hiện tại đã được chốt. Để tái lập một thí nghiệm mới, sao lưu kết quả cũ và dùng checkout/output riêng; evaluate_test.py từ chối ghi đè kết quả test đã có.

| Minh chứng | Vị trí |
|---|---|
| Nguồn và quy tắc tính trang | `data/manifest.json` |
| Cấu hình | `starter/experiment_config.json` |
| Benchmark/gold | `benchmark/questions.json` |
| Nhật ký | `artifacts/experiment_log.csv` |
| Trace và điểm dev/test | `starter/results/dev_*.json`, `starter/results/test_*.json` |
| Lựa chọn trước test | `starter/results/selection.json` |
| Coherence | `starter/results/coherence_audit.json`, `coherence_summary.json`, `coherence_review.md` |
| Metadata/grounding | `starter/results/test_audit.json`, `test_audit_summary.json`, `test_review.md` |
| Tài nguyên | `starter/results/resource_summary.json` |

Nhật ký CSV được điền sau lần chạy từ các file kết quả thật. Cột hypothesis mô tả mục đích thí nghiệm, không được coi là bằng chứng về thời điểm lập giả thuyết trước khi chạy.
