"""GUIDE.md, mục 1: tạo manifest nguồn và quy tắc tính trang từ dữ liệu thật."""
import hashlib
import json
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

from pypdf import PdfReader

BASE_DIR = Path(__file__).parent


def main():
    pdf_path = BASE_DIR / "data/thinkpython2.pdf"
    pages_path = BASE_DIR / "data/pages.json"
    reader = PdfReader(pdf_path)
    pages = json.loads(pages_path.read_text(encoding="utf-8"))
    if [p["page"] for p in pages] != list(range(111, 147)):
        raise ValueError("pages.json phải chứa đúng các trang PDF 111–146, không trùng.")

    page_records = []
    for page in pages:
        number = page["page"]
        raw = reader.pages[number - 1].extract_text() or ""
        normalized = unicodedata.normalize("NFC", raw)
        if normalized != page["text"]:
            raise ValueError(f"Trang {number}: pages.json không khớp cách chuẩn hóa của read_pdf.py.")
        if not normalized.strip():
            raise ValueError(f"Trang {number}: không có nội dung chữ để tính.")
        chapter = 10 if number <= 124 else 11 if number <= 136 else 12
        if page["document_id"] != "thinkpython2" or page["chapter"] != chapter:
            raise ValueError(f"Trang {number}: metadata không khớp.")
        page_records.append({
            "page_id": f"thinkpython2_p{number}",
            "pdf_page": number,
            "printed_page": number - 22,
            "chapter": chapter,
            "chapter_title": {10: "Lists", 11: "Dictionaries", 12: "Tuples"}[chapter],
            "character_count": len(normalized),
            "non_whitespace_character_count": sum(not c.isspace() for c in normalized),
            "extraction_status": "ok",
            "included": True
        })

    manifest = {
        "source_id": "thinkpython2",
        "title": "Think Python: How to Think Like a Computer Scientist",
        "author": "Allen B. Downey",
        "publisher": "Green Tea Press",
        "version": "2nd Edition, Version 2.4.1",
        "copyright_year": 2015,
        "source_path_or_url": "https://greenteapress.com/thinkpython2/thinkpython2.pdf",
        "local_path": "starter/data/thinkpython2.pdf",
        "language": "en",
        "license_or_permission": {
            "name": "Creative Commons Attribution-NonCommercial 3.0 Unported",
            "identifier": "CC-BY-NC-3.0",
            "url": "https://creativecommons.org/licenses/by-nc/3.0/",
            "evidence_pdf_page": 4,
            "usage": "Sao chép, chia sẻ và chỉnh sửa theo điều kiện giấy phép; ghi nguồn và dùng phi thương mại. Giữ ghi nguồn đối với nội dung bên thứ ba được dẫn trong sách.",
            "attribution": "Think Python, 2nd Edition, Version 2.4.1, Allen B. Downey, Copyright 2015 Allen Downey, Green Tea Press. https://greenteapress.com/thinkpython2/thinkpython2.pdf",
            "changes": "PDF gốc giữ nguyên. Văn bản được trích xuất bằng pypdf, chuẩn hóa Unicode NFC và chia chunk để tìm kiếm."
        },
        "accessed_at": datetime.now(timezone.utc).isoformat(),
        "accessed_at_note": "Thời điểm kiểm tra bản PDF local để lập manifest. Không ghi lại thời điểm tải file lần đầu.",
        "pdf_sha256": hashlib.sha256(pdf_path.read_bytes()).hexdigest(),
        "pages_json_sha256": hashlib.sha256(pages_path.read_bytes()).hexdigest(),
        "physical_page_count": len(reader.pages),
        "included_content_page_count": len(page_records),
        "included_pdf_pages": list(range(111, 147)),
        "counting_rule": "Chỉ tính 36 trang vật lý PDF 111–146, tương ứng trang in 89–124, gồm chương 10–12: giải thích, ví dụ, thuật ngữ và bài tập. Bìa, mục lục, trang trống và phần tài liệu tham khảo ngoài phạm vi này không được nạp. Không nhân bản trang. Ngưỡng 1.500 ký tự của đề dành cho đơn vị text không phân trang, không áp dụng cho trang PDF.",
        "character_count_rule": "Đếm ký tự sau chuẩn hóa NFC; gồm khoảng trắng và xuống dòng. Có thêm số ký tự không trắng để đối chiếu.",
        "total_characters": sum(p["character_count"] for p in page_records),
        "normalization": "Unicode NFC; giữ xuống dòng. Không gộp khoảng trắng hoặc tự sửa từ dính nhau.",
        "ocr_used": False,
        "empty_pages": [],
        "limitations": [
            "Sơ đồ khi trích xuất có thể trở thành chữ và số rời, không giữ bố cục hình.",
            "Một số tên hàm dính với từ bên cạnh hoặc từ bị ngắt dòng; NFC không tự sửa lỗi bố cục này.",
            "Nội dung là snapshot sách năm 2015; một số mô tả Python, ví dụ thứ tự dictionary, không phản ánh các phiên bản Python mới."
        ],
        "pages": page_records
    }
    output = BASE_DIR.parent / "data/manifest.json"
    output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Đã tạo {output}")
    print(f"PDF gốc: {len(reader.pages)} trang; sử dụng: {len(page_records)} trang nội dung.")
    print(f"Tổng ký tự: {manifest['total_characters']}.")
    print("Nguồn, giấy phép, số trang và ký tự từng trang đã được ghi vào manifest.")


if __name__ == "__main__":
    main()
