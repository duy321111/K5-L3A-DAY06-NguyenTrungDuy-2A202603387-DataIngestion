import json
from pathlib import Path
from sentence_transformers import SentenceTransformer

# Mục 3 trong GUIDE.md: tạo embedding thật, cùng model cho A và B.
data_dir = Path(__file__).parent / "data"

print("Đang nạp model...", flush=True)
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

for strategy in ["A", "B"]:
    input_path = data_dir / f"chunks_{strategy}.json"
    chunks = json.loads(input_path.read_text(encoding="utf-8"))

    # Lấy nội dung của từng chunk theo đúng thứ tự trong file.
    texts = [chunk["text"] for chunk in chunks]

    print(
        f"Đang tạo embedding cho {len(chunks)} chunk {strategy}...",
        flush=True
    )

    vectors = model.encode(
        texts,
        batch_size=16,
        show_progress_bar=True,
        normalize_embeddings=True
    )

    # Gắn vector vào đúng chunk tương ứng.
    for chunk, vector in zip(chunks, vectors):
        chunk["embedding"] = vector.tolist()

    output_path = data_dir / f"chunks_{strategy}_embedded.json"
    output_path.write_text(
        json.dumps(chunks, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"Đã lưu: {output_path}", flush=True)
for strategy in ["A", "B"]:
    path = data_dir / f"chunks_{strategy}_embedded.json"
    chunks = json.loads(path.read_text(encoding="utf-8"))

    dimensions = {len(chunk["embedding"]) for chunk in chunks}

    print(f"Cấu hình {strategy}: {len(chunks)} chunk")
    print("Số chiều embedding:", dimensions)