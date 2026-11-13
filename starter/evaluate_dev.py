"""GUIDE.md, mục 4: đánh giá 15 câu dev; chưa chạy bất kỳ câu test nào."""
import hashlib
import json
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

from search import MODEL_NAME, search_chunks

BASE_DIR = Path(__file__).parent
RESULTS_DIR = BASE_DIR / "results"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def canonical(text):
    """So sánh evidence sau chuẩn hóa Unicode và khoảng trắng."""
    return " ".join(unicodedata.normalize("NFC", text).split())


def gold_options(question):
    return [{
        "source_id": question["gold_source_id"],
        "page": question["gold_page"],
        "quote": question["evidence_quote"]
    }] + question.get("alternative_evidence", [])


def is_evidence_hit(question, hit):
    # Chỉ đúng trang chưa đủ: một chunk phải chứa trọn bằng chứng.
    return any(
        hit["document_id"] == gold["source_id"]
        and hit["page"] == gold["page"]
        and bool(canonical(gold["quote"]))
        and canonical(gold["quote"]) in canonical(hit["text"])
        for gold in gold_options(question)
    )


def validate_inputs(config, questions):
    if (config["model"] != MODEL_NAME or config["dimensions"] != 384
            or config["top_k"] != 3 or config["distance"] != "cosine"):
        raise ValueError("Config không khớp model/384 chiều/top-3/cosine của pipeline hiện tại.")
    if config["strategies"] != {
        "A": {"chunking": "fixed_size", "chunk_size": 500, "overlap": 50, "use_filter": False},
        "B": {"chunking": "section", "max_chunk_size": 1000, "use_filter": False},
        "C": {"chunks_from": "B", "use_filter": True, "filter_field": "chapter"}
    }:
        raise ValueError("Cấu hình đã thay đổi; cần kiểm tra lại chunking/search trước khi đánh giá.")
    if len(questions) < 15 or len({q["id"] for q in questions}) != len(questions):
        raise ValueError("Cần ít nhất 15 câu dev có ID riêng.")

    pages = {(p["document_id"], p["page"]): p for p in read_json(BASE_DIR / "data/pages.json")}
    for question in questions:
        if not question["question"].strip() or not question["expected_answer"].strip():
            raise ValueError(f"{question['id']}: câu hỏi/đáp án rỗng.")
        filters = question.get("filter", {})
        if not isinstance(filters, dict) or set(filters) - {"chapter"}:
            raise ValueError("Hiện chỉ hỗ trợ filter chapter.")
        if filters and (type(filters["chapter"]) is not int or filters["chapter"] not in (10, 11, 12)):
            raise ValueError("chapter phải là 10, 11 hoặc 12.")
        for gold in gold_options(question):
            page = pages.get((gold["source_id"], gold["page"]))
            if not page or not canonical(gold["quote"]) or canonical(gold["quote"]) not in canonical(page["text"]):
                raise ValueError(f"{question['id']}: không thấy evidence ở đúng trang nguồn.")
            if filters and filters["chapter"] != page["chapter"]:
                raise ValueError(f"{question['id']}: filter không khớp chương trong nguồn.")

    # Kiểm tra dữ liệu database vẫn khớp các file chunk đã tạo.
    import pg8000.native
    connection = pg8000.native.Connection(user="day6", password="day6_local_only",
                 host="127.0.0.1", port=55433, database="day6_lab", timeout=10)
    counts = {}
    try:
        for strategy in ("A", "B"):
            originals = read_json(BASE_DIR / f"data/chunks_{strategy}.json")
            expected = {c["chunk_id"]: (c["document_id"], c["source"], c["page"], c["chapter"], c["text"]) for c in originals}
            rows = connection.run(
                """SELECT chunk_id, document_id, source, page, chapter, content,
                          vector_dims(embedding) FROM chunks WHERE strategy = :strategy""",
                strategy=strategy
            )
            actual = {r[0]: tuple(r[1:6]) for r in rows}
            if expected != actual or any(r[6] != 384 for r in rows):
                raise ValueError(f"Dữ liệu {strategy} trong database không khớp JSON. Chạy lại các bước tạo và nạp embedding.")
            counts[strategy] = len(rows)
    finally:
        connection.close()
    counts["C"] = counts["B"]
    return counts


def main():
    config_path = BASE_DIR / "experiment_config.json"
    benchmark_path = BASE_DIR.parent / "benchmark/questions.json"
    config = read_json(config_path)
    # Lọc dev trước khi tạo vector/tìm kiếm. Test được để dành.
    questions = [q for q in read_json(benchmark_path) if q["split"] == "dev"]
    counts = validate_inputs(config, questions)
    print(f"Đã xác minh {len(questions)} câu dev và dữ liệu database.", flush=True)

    from sentence_transformers import SentenceTransformer
    print("Đang nạp model...", flush=True)
    model = SentenceTransformer(config["model"])
    texts = [q["question"] for q in questions]
    if any(len(model.tokenizer(text, truncation=False)["input_ids"]) > model.max_seq_length for text in texts):
        raise ValueError("Có câu hỏi vượt giới hạn token của model.")
    started = time.perf_counter()
    # Mỗi câu chỉ tạo vector một lần, dùng chung cho A/B/C.
    vectors = model.encode(texts, normalize_embeddings=True, show_progress_bar=True).tolist()
    embedding_seconds = time.perf_counter() - started

    traces, metrics = [], []
    for strategy in ("A", "B", "C"):
        strategy_traces = []
        for question, vector in zip(questions, vectors):
            requested_filter = question.get("filter", {})
            applied_filter = requested_filter if strategy == "C" else {}
            start = time.perf_counter()
            # Chỉ vector câu hỏi và filter đã cung cấp được truyền vào tìm kiếm.
            hits = search_chunks(vector, strategy, applied_filter.get("chapter"))
            search_seconds = time.perf_counter() - start
            for rank, hit in enumerate(hits, 1):
                hit["rank"] = rank
                hit["evidence_hit"] = is_evidence_hit(question, hit)
            trace = {
                "strategy": strategy, "split": "dev", "question_id": question["id"],
                "question": question["question"], "expected_answer": question["expected_answer"],
                "gold_evidence": gold_options(question), "requested_filter": requested_filter,
                "applied_filter": applied_filter, "hits": hits,
                "hit_at_1": bool(hits and hits[0]["evidence_hit"]),
                "evidence_hit_at_3": any(h["evidence_hit"] for h in hits),
                "search_seconds": search_seconds
            }
            strategy_traces.append(trace)
        traces.extend(strategy_traces)
        n = len(strategy_traces)
        hit1 = sum(t["hit_at_1"] for t in strategy_traces)
        hit3 = sum(t["evidence_hit_at_3"] for t in strategy_traces)
        metrics.append({"strategy": strategy, "split": "dev", "questions": n,
                        "hit1_count": hit1, "hit3_count": hit3,
                        "hit_at_1": hit1 / n, "evidence_hit_at_3": hit3 / n,
                        "chunk_count": counts[strategy]})
        print(f"{strategy}: Hit@1 = {hit1}/{n}; Evidence Hit@3 = {hit3}/{n}", flush=True)

    RESULTS_DIR.mkdir(exist_ok=True)
    def save(name, data):
        (RESULTS_DIR / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    save("dev_traces.json", traces)
    save("dev_metrics.json", metrics)
    files = [config_path, benchmark_path, BASE_DIR / "search.py", Path(__file__),
             BASE_DIR / "data/pages.json", BASE_DIR / "data/thinkpython2.pdf",
             BASE_DIR / "data/chunks_A_embedded.json", BASE_DIR / "data/chunks_B_embedded.json"]
    save("dev_run.json", {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "config": config, "split": "dev", "query_embedding_seconds": embedding_seconds,
        "model_max_tokens": model.max_seq_length, "api_cost_usd": 0,
        "cost_note": "Local inference; electricity/hardware cost not measured.",
        "input_sha256": {str(p.relative_to(BASE_DIR.parent)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
        "metric_note": "Strict full-quote evidence match in one source/page chunk after NFC/whitespace normalization. No manual grounding/coherence labels inferred."
    })
    print("Đã lưu dev_traces.json, dev_metrics.json, dev_run.json trong starter/results/.")
    print("Chưa chạy test. Đọc kết quả dev trước khi chốt chiến lược.")


if __name__ == "__main__":
    main()
