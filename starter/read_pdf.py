from pathlib import Path
import unicodedata
from pypdf import PdfReader

# Tìm PDF trong thư mục data cạnh file Python này
pdf_path = Path(__file__).parent / "data" / "thinkpython2.pdf"

reader = PdfReader(pdf_path)

print("Tổng số trang:", len(reader.pages))
pages = []
# Python đếm từ 0, nên trang PDF 111 có chỉ số 110
for page_number in range(111, 147):
    text = reader.pages[page_number - 1].extract_text() or ""
    text = unicodedata.normalize("NFC", text)
    if not text:
        print(f"CẢNH BÁO: Trang {page_number} không lấy được chữ.")
    if page_number <= 124:
        chapter = 10
    elif page_number <= 136:
        chapter = 11
    else:
        chapter = 12

    pages.append({
        "document_id": "thinkpython2",
        "source": "https://greenteapress.com/thinkpython2/thinkpython2.pdf",
        "page": page_number,
        "chapter": chapter,
        "text": text,
        "extraction_status": "ok" if text else "empty"
    })
    print(f"\n--- Trang {page_number} ---")
    print(text[:200])
import json

output_path = Path(__file__).parent / "data" / "pages.json"

output_path.write_text(
    json.dumps(pages, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print(f"Đã lưu {len(pages)} trang vào {output_path}")