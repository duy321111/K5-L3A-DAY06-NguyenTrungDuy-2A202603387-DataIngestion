# Chạy pipeline PostgreSQL + pgvector

Xem [README ở gốc repo](../README.md) để cài môi trường và chạy đầy đủ từng bước.

Pipeline đã triển khai bằng các script ngay trong `starter/`, dùng **pg8000** kết nối PostgreSQL trong Docker và **Sentence Transformers** để tạo embedding local. Không cần API key.

Từ thư mục gốc, cài thư viện:

```powershell
.\.venv\Scripts\python.exe -m pip install -r starter/requirements.txt
cd starter
```

Từ `starter/`, khởi động database và nạp các file embedding đã có:

```powershell
docker compose -p day6_student_starter up -d --wait
Get-Content -Raw create_tables.sql | docker compose -p day6_student_starter exec -T postgres psql -U day6 -d day6_lab -v ON_ERROR_STOP=1
..\.venv\Scripts\python.exe check_database.py
..\.venv\Scripts\python.exe check_embeddings.py
..\.venv\Scripts\python.exe load_database.py
..\.venv\Scripts\python.exe search.py
```

Nếu Terminal đã có `(.venv)`, có thể dùng `python` thay đường dẫn dài. Kết quả database cần có 151 chunk A và 104 chunk B; C dùng chung B và thêm filter lúc tìm kiếm.

Để đọc kết quả đã chạy: mở `results/dev_metrics.json`, `results/test_metrics.json` và [báo cáo cá nhân](../report/individual/2A202603387_NguyenTrungDuy.md). Không cần chạy lại test.

`src/` và `scripts/check_setup.py` giữ lại từ bộ khung đề bài. Chương trình hiện tại chạy qua các script được liệt kê trong README gốc; `python -m src.run` vẫn là khung TODO.
