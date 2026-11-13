import json
from pathlib import Path

data_dir = Path(__file__).parent / "data"
pages = json.loads((data_dir / "pages.json").read_text(encoding="utf-8"))

chunks = []

for page in pages:
    text = page["text"]

    for start in range(0, len(text), 450):
        chunk_text = text[start:start + 500]

        chunks.append({
            "chunk_id": f"thinkpython2_p{page['page']}_{start}",
            "document_id": page["document_id"],
            "source": page["source"],
            "page": page["page"],
            "chapter": page["chapter"],
            "text": chunk_text
        })

        if start + 500 >= len(text):
            break

output_path = data_dir / "chunks_A.json"
output_path.write_text(
    json.dumps(chunks, ensure_ascii=False, indent=2),
    encoding="utf-8"
)
first_page = pages[0]["text"]

print("Số dòng trống ở trang 111:", first_page.count("\n\n"))
print(f"Đã tạo {len(chunks)} đoạn.")