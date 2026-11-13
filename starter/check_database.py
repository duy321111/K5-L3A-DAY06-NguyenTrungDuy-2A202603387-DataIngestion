"""GUIDE.md, mục 3: kiểm tra kết nối PostgreSQL và pgvector, chưa nạp dữ liệu."""
import pg8000.native

# Thông tin của database local trong docker-compose.yml.
# 127.0.0.1 là máy của bạn; 55433 là cổng Docker mở ra cho Python kết nối.
connection = pg8000.native.Connection(
    user="day6",
    password="day6_local_only",
    host="127.0.0.1",
    port=55433,
    database="day6_lab",
    timeout=10
)

try:
    # Chỉ đọc phiên bản pgvector, không thêm/xóa dữ liệu.
    result = connection.run(
        "SELECT extversion FROM pg_extension WHERE extname = 'vector'"
    )

    print("Kết nối PostgreSQL thành công!")
    if result:
        print("Phiên bản pgvector:", result[0][0])
    else:
        raise RuntimeError("Database chưa bật extension vector.")
finally:
    # Luôn đóng kết nối sau khi kiểm tra.
    connection.close()
