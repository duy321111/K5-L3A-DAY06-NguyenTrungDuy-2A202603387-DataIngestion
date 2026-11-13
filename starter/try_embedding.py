from sentence_transformers import SentenceTransformer

# 1. Nạp model; lần đầu cần tải từ Internet
print("Đang nạp model...", flush=True)

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

# 2. Câu cần chuyển thành embedding
text = "How do I remove an item from a list?"

# 3. Model tính vector biểu diễn câu
print("Đang tạo embedding...", flush=True)

vector = model.encode(text)

# 4. In kết quả
print("\nCâu gốc:", text)
print("Số chiều:", len(vector))
print("Toàn bộ embedding:")
print(vector.tolist())