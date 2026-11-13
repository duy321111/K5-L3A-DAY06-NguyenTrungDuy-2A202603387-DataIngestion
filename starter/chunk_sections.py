import json
import re
from pathlib import Path

data_dir = Path(__file__).parent / "data"
pages = json.loads(
    (data_dir / "pages.json").read_text(encoding="utf-8")
)

chunks = []

for page in pages:
    text = page["text"]

    # Tìm vị trí bắt đầu của từng tiêu đề mục
    headings = list(re.finditer(
        r"^\d+\.\d+\s+[^\n]+",
        text,
        flags=re.MULTILINE
    ))

    boundaries = sorted(set(
        [0] + [heading.start() for heading in headings] + [len(text)]
    ))

    for i in range(len(boundaries) - 1):
        section_text = text[boundaries[i]:boundaries[i + 1]]

        # Mục dài được chia nhỏ, tối đa 1.000 ký tự
        for start in range(0, len(section_text), 1000):
            chunk_text = section_text[start:start + 1000].strip()

            if not chunk_text:
                continue

            chunks.append({
                "chunk_id": f"thinkpython2_B_p{page['page']}_{i}_{start}",
                "document_id": page["document_id"],
                "source": page["source"],
                "page": page["page"],
                "chapter": page["chapter"],
                "text": chunk_text
            })

output_path = data_dir / "chunks_B.json"
output_path.write_text(
    json.dumps(chunks, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print(f"Đã tạo {len(chunks)} đoạn cho cấu hình B.")

print("Độ dài đoạn lớn nhất:", max((len(c["text"]) for c in chunks), default=0))
print("Số đoạn rỗng:", sum(not c["text"].strip() for c in chunks))
print("Số trang có chunk:", len(set(c["page"] for c in chunks)))
