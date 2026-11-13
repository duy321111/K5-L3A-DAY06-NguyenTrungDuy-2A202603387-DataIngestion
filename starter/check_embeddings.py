import json
import math
from pathlib import Path

# Mục 3 trong GUIDE.md: kiểm tra embedding trước khi lưu vào database.
data_dir = Path(__file__).parent / "data"

for strategy in ["A", "B"]:
    input_path = data_dir / f"chunks_{strategy}.json"
    embedded_path = data_dir / f"chunks_{strategy}_embedded.json"

    original_chunks = json.loads(input_path.read_text(encoding="utf-8"))
    chunks = json.loads(embedded_path.read_text(encoding="utf-8"))

    if len(chunks) != len(original_chunks):
        raise ValueError(f"Cấu hình {strategy}: số chunk trước/sau embedding không khớp.")
    if not chunks:
        raise ValueError(f"Cấu hình {strategy}: không có chunk để kiểm tra.")

    for original, chunk in zip(original_chunks, chunks):
        if {k: v for k, v in chunk.items() if k != "embedding"} != original:
            raise ValueError(f"Cấu hình {strategy}: nội dung hoặc metadata của chunk đã thay đổi.")

        vector = chunk.get("embedding")
        if not isinstance(vector, list) or len(vector) != 384:
            raise ValueError(f"Chunk {chunk['chunk_id']}: embedding phải có 384 số.")
        if not all(type(value) in (int, float) and math.isfinite(value) for value in vector):
            raise ValueError(f"Chunk {chunk['chunk_id']}: embedding chứa giá trị không hợp lệ.")
        if not any(value != 0 for value in vector):
            raise ValueError(f"Chunk {chunk['chunk_id']}: embedding không được toàn số 0.")

    dimensions = {len(chunk["embedding"]) for chunk in chunks}
    print(f"Cấu hình {strategy}: {len(chunks)} chunk")
    print("Số chiều embedding:", dimensions)
    print("Nội dung, metadata và vector: hợp lệ.\n")
