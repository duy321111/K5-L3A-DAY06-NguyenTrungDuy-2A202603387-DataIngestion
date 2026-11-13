"""GUIDE.md, mục 4.2: tạo mẫu chấm coherence, không tự tạo nhãn thủ công."""
import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent
RESULTS_DIR = BASE_DIR / "results"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def chunk_offset(chunk, page_text, strategy):
    parts = chunk["chunk_id"].split("_")
    if strategy == "A":
        start = int(parts[-1])
    else:
        headings = list(re.finditer(r"^\d+\.\d+\s+[^\n]+", page_text, re.MULTILINE))
        boundaries = sorted(set([0] + [h.start() for h in headings] + [len(page_text)]))
        section_index, offset = int(parts[-2]), int(parts[-1])
        raw_start = boundaries[section_index] + offset
        raw_end = min(raw_start + 1000, boundaries[section_index + 1])
        raw = page_text[raw_start:raw_end]
        start = raw_start + len(raw) - len(raw.lstrip())
    if page_text[start:start + len(chunk["text"])] != chunk["text"]:
        raise ValueError("Chunk không khớp vị trí trong pages.json; kiểm tra lại dữ liệu.")
    return start


def main():
    pages = sorted(read_json(BASE_DIR / "data/pages.json"), key=lambda p: p["page"])[:10]
    if len(pages) != 10:
        raise ValueError("Cần đủ 10 vị trí nguồn để lấy mẫu.")
    chunk_sets = {s: read_json(BASE_DIR / f"data/chunks_{s}.json") for s in ("A", "B")}
    rule = (
        "Lấy 10 trang vật lý đầu tiên theo thứ tự tăng dần (111–120). "
        "Mỗi trang lấy ký tự không trắng đầu tiên từ vị trí giữa trang trở đi làm mốc. "
        "Nếu nhiều chunk bao phủ mốc, chọn chunk bắt đầu sớm nhất, rồi theo chunk_id. "
        "C dùng cùng chunk của B. Quy tắc không dựa vào điểm retrieval; xác định trước khi chấm coherence."
    )
    samples=[]
    lines=["# Chấm độ mạch lạc của chunk", "", "Yêu cầu: GUIDE.md, mục 4.2 — Chunk coherence.", "", rule, "",
           "## Cách chấm", "", "- 0: bị cắt giữa ý hoặc thiếu chủ thể, không hiểu được.",
           "- 1: hiểu một phần nhưng còn thiếu ngữ cảnh.", "- 2: tự hiểu được và giữ trọn ý.", "",
           "Đọc chunk như một đoạn đứng riêng, sau đó đối chiếu nguồn. Ghi score, reason và reviewer trong coherence_audit.json.",
           "Không dùng Hit@3 thay điểm này. B/C cùng chunk nên điểm coherence cần nhất quán. Đây không phải chấm khả năng trả lời câu hỏi.", ""]
    for page in pages:
        text=page["text"]
        anchor=next((i for i in range(len(text)//2,len(text)) if not text[i].isspace()), None)
        if anchor is None:
            raise ValueError("Không tìm được mốc nội dung giữa trang.")
        lines += [f"## Trang PDF {page['page']} — mốc ký tự {anchor} (đếm từ 0)", "",
                  "### Nội dung trang nguồn để đối chiếu", "", "```text", text, "```", ""]
        for strategy in ("A","B","C"):
            stored_strategy="B" if strategy=="C" else strategy
            candidates=[]
            for chunk in chunk_sets[stored_strategy]:
                if chunk["page"] != page["page"]:
                    continue
                start=chunk_offset(chunk,text,stored_strategy)
                if start <= anchor < start+len(chunk["text"]):
                    candidates.append((start,chunk["chunk_id"],chunk))
            if not candidates:
                raise ValueError(f"Không có chunk {strategy} chứa mốc trang {page['page']}.")
            start,chunk_id,chunk=min(candidates,key=lambda item:(item[0],item[1]))
            sample_id=f"{strategy}_p{page['page']}"
            samples.append({
                "sample_id":sample_id,"strategy":strategy,"document_id":page["document_id"],
                "source":page["source"],"page":page["page"],"chapter":page["chapter"],
                "anchor_character":anchor,"chunk_id":chunk_id,"chunk_start":start,
                "chunk_text":chunk["text"],"score":None,"reason":"","reviewer":""
            })
            lines += [f"### {sample_id}", "", f"Chunk: `{chunk_id}`; bắt đầu ở ký tự {start}.", "",
                      "```text", chunk["text"], "```", "", "Điểm: chưa chấm. Lý do: chưa điền.", ""]

    RESULTS_DIR.mkdir(exist_ok=True)
    audit_path=RESULTS_DIR/"coherence_audit.json"
    if audit_path.exists() and any(r.get("score") is not None for r in read_json(audit_path)["samples"]):
        print("Đã có nhãn coherence; giữ nguyên file để không mất điểm và thông tin người chấm.")
        return
    if audit_path.exists():
        old={r["sample_id"]:r for r in read_json(audit_path)["samples"]}
        for sample in samples:
            previous=old.get(sample["sample_id"])
            if previous:
                fixed_keys=set(sample)-{"score","reason","reviewer"}
                if any(sample[k]!=previous.get(k) for k in fixed_keys):
                    raise ValueError("Mẫu đã thay đổi; không ghi đè nhãn cũ.")
                for key in ("score","reason","reviewer","review_method","learner_confirmed"):
                    if key in previous:
                        sample[key]=previous[key]
    audit_path.write_text(json.dumps({"sampling_rule":rule,"samples":samples},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (RESULTS_DIR/"coherence_review.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(f"Đã chuẩn bị {len(samples)} mẫu: 10 vị trí nguồn × A/B/C.")
    print("Đọc starter/results/coherence_review.md; điền nhãn vào coherence_audit.json.")
    print("Không có điểm thủ công nào được tự tạo. Nhãn đã điền được giữ lại khi chạy lại.")


if __name__=="__main__":
    main()
