"""GUIDE.md, mục 4.3–4.4: chuẩn bị kiểm tra metadata và grounding của test."""
import hashlib
import json
from pathlib import Path

BASE_DIR=Path(__file__).parent
RESULTS_DIR=BASE_DIR/"results"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    output=RESULTS_DIR/"test_audit.json"
    if output.exists():
        raise ValueError("Đã có test_audit.json; giữ nguyên để không mất nhãn đã điền.")
    trace_path=RESULTS_DIR/"test_traces.json"
    traces=read_json(trace_path)
    pages={(p["document_id"],p["page"]):p for p in read_json(BASE_DIR/"data/pages.json")}
    if len(traces)!=15 or any(t["split"]!="test" for t in traces):
        raise ValueError("Cần đúng 5 câu test × 3 cấu hình.")
    if any(len([t for t in traces if t["strategy"]==s])!=5 for s in ("A","B","C")):
        raise ValueError("Thiếu test của một cấu hình.")
    samples=[]
    source_pages=set()
    lines=["# Kiểm tra metadata và grounding của kết quả test", "",
           "Yêu cầu: GUIDE.md, mục 4.3–4.4. Cùng 5 câu test được đánh giá trên A/B/C.", "",
           "## Cách điền test_audit.json", "",
           "- grounding_score: 0 = không có bằng chứng; 1 = có nhưng thiếu điều kiện/ngữ cảnh; 2 = đủ trả lời và truy nguồn.",
           "- grounding_reason: giải thích vì sao top-3 đủ hoặc thiếu bằng chứng; ghi chunk/trang liên quan.",
           "- metadata_correct: true/false cho mỗi hit sau khi đối chiếu source, page, chapter với trang nguồn.",
           "- metadata_reason: ghi điều đã đối chiếu hoặc lỗi tìm thấy.",
           "- filter_compliant: true/false cho mỗi hit nếu requested_filter không rỗng; nếu không yêu cầu filter thì giữ null (N/A).",
           "- reviewer: người thực sự đọc và chấm. Các nhãn khởi tạo null, chưa được chấm.", "",
           "Grounding xét tổng hợp cả 3 đoạn, khác với metric exact-quote trong một chunk. "
           "Không tự đổi evidence_hit thành điểm grounding. A/B không áp dụng filter nhưng vẫn có thể kiểm tra phạm vi kết quả khi câu hỏi yêu cầu.", ""]
    for trace in traces:
        sample_id=f"{trace['strategy']}_{trace['question_id']}"
        hits=trace["hits"]
        if len(hits)!=3:
            raise ValueError("Trace phải giữ đầy đủ top-3 cho bộ test này.")
        samples.append({
            "sample_id":sample_id,"strategy":trace["strategy"],"question_id":trace["question_id"],
            "question":trace["question"],"expected_answer":trace["expected_answer"],
            "requested_filter":trace["requested_filter"],"applied_filter":trace["applied_filter"],
            "gold_evidence":trace["gold_evidence"],"grounding_score":None,
            "grounding_reason":"","reviewer":"","metadata_audit":[{
                "rank":h["rank"],"chunk_id":h["chunk_id"],"document_id":h["document_id"],
                "source":h["source"],"page":h["page"],"chapter":h["chapter"],
                "text":h["text"],"metadata_correct":None,"metadata_reason":"",
                "filter_compliant":None
            } for h in hits]
        })
        lines += [f"## {sample_id}", "", "**Câu hỏi:** "+trace["question"], "",
                  "**Đáp án mong đợi:** "+trace["expected_answer"], "",
                  "Filter yêu cầu: `"+json.dumps(trace["requested_filter"])+"`; filter thực sự áp dụng: `"+json.dumps(trace["applied_filter"])+"`.", "",
                  "### Bằng chứng nguồn đã ghi trong benchmark", ""]
        for gold in trace["gold_evidence"]:
            source_pages.add((gold["source_id"],gold["page"]))
            lines += [f"Trang PDF {gold['page']} — {gold['source_id']}:", "", "> "+gold["quote"], ""]
        for h in hits:
            source_pages.add((h["document_id"],h["page"]))
            if (h["document_id"],h["page"]) not in pages:
                raise ValueError("Kết quả không truy được trang nguồn.")
            lines += [f"### Kết quả {h['rank']}: {h['chunk_id']}", "",
                      f"Nguồn: {h['source']}", f"Trang PDF: {h['page']}; chương: {h['chapter']}.", "",
                      "```text",h["text"],"```", ""]
        lines += ["**Nhãn đánh giá:** chưa chấm; điền trong test_audit.json.", ""]
    lines += ["# Phụ lục: văn bản từng trang nguồn để đối chiếu", "",
              "Số trang ở đây là trang vật lý trong file PDF. Metadata chương và bản trích xuất có thể kiểm tra lại bằng PDF gốc.", ""]
    for key in sorted(source_pages):
        page=pages[key]
        lines += [f"## Trang PDF {page['page']} — chương {page['chapter']}", "",
                  "Nguồn: "+page["source"], "", "```text",page["text"],"```", ""]
    output.write_text(json.dumps({
        "status":"Unscored review material; no human or AI assessment labels assigned",
        "trace_sha256":hashlib.sha256(trace_path.read_bytes()).hexdigest(),
        "metadata_unit":"Each retrieved record; 15 records per strategy",
        "filter_unit":"A question passes if all returned hits satisfy requested_filter; no filter is N/A",
        "grounding_unit":"Joint evidence in top-3 for each question/strategy; 5 cases per strategy",
        "samples":samples
    },ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (RESULTS_DIR/"test_review.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print("Đã tạo test_review.md và test_audit.json: 15 trường hợp, 45 bản ghi metadata; nhãn đều để trống.")


if __name__=="__main__":
    main()
