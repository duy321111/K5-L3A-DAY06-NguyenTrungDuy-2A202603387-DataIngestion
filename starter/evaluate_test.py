"""GUIDE.md, mục 4: chốt theo dev trước, sau đó đánh giá test riêng biệt."""
import hashlib
import json
import math
import time
from datetime import datetime, timezone
from pathlib import Path

from evaluate_dev import (
    BASE_DIR, RESULTS_DIR, canonical, gold_options,
    is_evidence_hit, read_json, validate_inputs
)
from search import search_chunks


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def check_files(hashes):
    for name, expected in hashes.items():
        path = BASE_DIR.parent / Path(name.replace("\\", "/"))
        if sha(path) != expected:
            raise ValueError(f"File đã thay đổi sau dev/chốt cấu hình: {name}. Không dùng test để chỉnh bài.")


def verify_database_vectors():
    """Đối chiếu cả giá trị vector, ngoài metadata đã kiểm tra ở bước dev."""
    import pg8000.native
    connection = pg8000.native.Connection(user="day6", password="day6_local_only",
                 host="127.0.0.1", port=55433, database="day6_lab", timeout=10)
    try:
        for strategy in ("A", "B"):
            expected = {c["chunk_id"]: c for c in read_json(BASE_DIR / f"data/chunks_{strategy}_embedded.json")}
            rows = connection.run(
                "SELECT chunk_id, embedding::text FROM chunks WHERE strategy = :strategy ORDER BY chunk_id",
                strategy=strategy
            )
            if {r[0] for r in rows} != set(expected):
                raise ValueError("Các chunk database không khớp snapshot embedding.")
            for chunk_id, vector_text in rows:
                actual = json.loads(vector_text)
                original = expected[chunk_id]["embedding"]
                if len(actual) != len(original) or not all(
                    math.isclose(a, b, rel_tol=1e-6, abs_tol=1e-8)
                    for a, b in zip(actual, original)
                ):
                    raise ValueError(f"Vector database khác snapshot: {strategy}/{chunk_id}")
    finally:
        connection.close()


def freeze_selection(config):
    dev_run = read_json(RESULTS_DIR / "dev_run.json")
    check_files(dev_run["input_sha256"])
    if dev_run["config"] != config:
        raise ValueError("Config hiện tại khác lần chạy dev.")
    dev_metrics = read_json(RESULTS_DIR / "dev_metrics.json")
    dev_traces = read_json(RESULTS_DIR / "dev_traces.json")
    if {r["strategy"] for r in dev_metrics} != {"A", "B", "C"} or len(dev_metrics) != 3:
        raise ValueError("Thiếu bảng dev A/B/C.")
    for metric in dev_metrics:
        traces = [t for t in dev_traces if t["strategy"] == metric["strategy"]]
        if (any(t["split"] != "dev" for t in traces)
                or len(traces) != metric["questions"]
                or sum(t["hit_at_1"] for t in traces) != metric["hit1_count"]
                or sum(t["evidence_hit_at_3"] for t in traces) != metric["hit3_count"]):
            raise ValueError("Bảng dev không khớp trace.")
        if metric["hit_at_1"] != metric["hit1_count"] / metric["questions"] or metric["evidence_hit_at_3"] != metric["hit3_count"] / metric["questions"]:
            raise ValueError("Tỷ lệ dev không khớp số câu đúng.")

    chosen = min(dev_metrics, key=lambda m: (
        -m["evidence_hit_at_3"], -m["hit_at_1"], m["chunk_count"], m["strategy"]
    ))["strategy"]
    locked_files = dict(dev_run["input_sha256"])
    for name in ("dev_run.json", "dev_metrics.json", "dev_traces.json"):
        path = RESULTS_DIR / name
        locked_files[path.relative_to(BASE_DIR.parent).as_posix()] = sha(path)
    locked_files[Path(__file__).relative_to(BASE_DIR.parent).as_posix()] = sha(Path(__file__))
    selection_path = RESULTS_DIR / "selection.json"
    if selection_path.exists():
        selection = read_json(selection_path)
        check_files(selection["frozen_sha256"])
        if selection["chosen_strategy"] != chosen:
            raise ValueError("Lựa chọn đã khóa không khớp dev.")
    else:
        selection = {
            "frozen_at": datetime.now(timezone.utc).isoformat(),
            "chosen_strategy": chosen,
            "selection_rule": config["selection_rule"],
            "basis": "Dev results only; no test retrieval executed before this file was written.",
            "dev_metrics": dev_metrics,
            "frozen_sha256": locked_files,
            "note": "Same-book dev/test topics overlap; small illustrative holdout, not broad generalization."
        }
        save(selection_path, selection)
    print(f"Đã chốt cấu hình {chosen} theo dev; không chọn lại bằng điểm test.", flush=True)
    return selection, dev_run


def main():
    if any((RESULTS_DIR / name).exists() for name in ("test_traces.json", "test_metrics.json", "test_run.json")):
        raise ValueError("Đã có kết quả test. Giữ lại bản gốc, không ghi đè để tinh chỉnh theo test.")
    config = read_json(BASE_DIR / "experiment_config.json")
    all_questions = read_json(BASE_DIR.parent / "benchmark/questions.json")
    dev_questions = [q for q in all_questions if q["split"] == "dev"]
    counts = validate_inputs(config, dev_questions)
    verify_database_vectors()
    # Ghi lựa chọn trước khi nạp model/tìm kiếm bất kỳ câu test nào.
    selection, dev_run = freeze_selection(config)

    questions = [q for q in all_questions if q["split"] == "test"]
    if len(questions) < 5 or len({q["id"] for q in all_questions}) != len(all_questions):
        raise ValueError("Cần >=5 test và ID duy nhất trong benchmark.")
    if not any(q.get("filter") for q in questions):
        raise ValueError("Cần ít nhất một câu test có filter.")
    pages = {(p["document_id"], p["page"]): p for p in read_json(BASE_DIR / "data/pages.json")}
    for question in questions:
        filters = question.get("filter", {})
        if not isinstance(filters, dict) or set(filters) - {"chapter"}:
            raise ValueError("Chỉ hỗ trợ filter chapter.")
        if filters and (type(filters["chapter"]) is not int or filters["chapter"] not in (10, 11, 12)):
            raise ValueError("Filter chapter không hợp lệ.")
        if not question["question"].strip() or not question["expected_answer"].strip():
            raise ValueError("Câu hỏi/đáp án test rỗng.")
        for gold in gold_options(question):
            page = pages.get((gold["source_id"], gold["page"]))
            if not page or not canonical(gold["quote"]) or canonical(gold["quote"]) not in canonical(page["text"]):
                raise ValueError(f"{question['id']}: thiếu bằng chứng ở trang nguồn.")
            if filters and filters["chapter"] != page["chapter"]:
                raise ValueError("Filter không khớp chương nguồn.")

    from sentence_transformers import SentenceTransformer
    print("Đang nạp cùng model để chạy test...", flush=True)
    model = SentenceTransformer(config["model"])
    if model.max_seq_length != dev_run["model_max_tokens"]:
        raise ValueError("Giới hạn model khác lần chạy dev.")
    texts = [q["question"] for q in questions]
    if any(len(model.tokenizer(text, truncation=False)["input_ids"]) > model.max_seq_length for text in texts):
        raise ValueError("Câu hỏi test vượt giới hạn token.")
    start = time.perf_counter()
    vectors = model.encode(texts, normalize_embeddings=True, show_progress_bar=True).tolist()
    embedding_seconds = time.perf_counter() - start
    traces, metrics = [], []
    for strategy in ("A", "B", "C"):
        rows = []
        for question, vector in zip(questions, vectors):
            requested_filter = question.get("filter", {})
            applied_filter = requested_filter if strategy == "C" else {}
            start = time.perf_counter()
            hits = search_chunks(vector, strategy, applied_filter.get("chapter"))
            search_seconds = time.perf_counter() - start
            for rank, hit in enumerate(hits, 1):
                hit["rank"] = rank
                hit["evidence_hit"] = is_evidence_hit(question, hit)
            rows.append({
                "strategy": strategy, "split": "test", "question_id": question["id"],
                "question": question["question"], "expected_answer": question["expected_answer"],
                "gold_evidence": gold_options(question), "requested_filter": requested_filter,
                "applied_filter": applied_filter, "hits": hits,
                "hit_at_1": bool(hits and hits[0]["evidence_hit"]),
                "evidence_hit_at_3": any(h["evidence_hit"] for h in hits),
                "search_seconds": search_seconds
            })
        traces.extend(rows)
        n = len(rows)
        hit1 = sum(r["hit_at_1"] for r in rows)
        hit3 = sum(r["evidence_hit_at_3"] for r in rows)
        metrics.append({"strategy": strategy, "split": "test", "questions": n,
                        "hit1_count": hit1, "hit3_count": hit3,
                        "hit_at_1": hit1 / n, "evidence_hit_at_3": hit3 / n,
                        "chunk_count": counts[strategy]})
        print(f"{strategy}: Hit@1 = {hit1}/{n}; Evidence Hit@3 = {hit3}/{n}", flush=True)

    check_files(selection["frozen_sha256"])
    save(RESULTS_DIR / "test_traces.json", traces)
    save(RESULTS_DIR / "test_metrics.json", metrics)
    save(RESULTS_DIR / "test_run.json", {
        "created_at": datetime.now(timezone.utc).isoformat(), "split": "test",
        "chosen_strategy_from_dev": selection["chosen_strategy"],
        "selection_sha256": sha(RESULTS_DIR / "selection.json"),
        "query_embedding_seconds": embedding_seconds,
        "config": config, "api_cost_usd": 0,
        "cost_note": "Local inference; electricity/hardware cost not measured.",
        "resolved_model_revision": getattr(model._first_module().auto_model.config, "_commit_hash", None),
        "note": "Strict quote proxy; human coherence/metadata/grounding audit still required."
    })
    print("Đã lưu selection.json, test_traces.json, test_metrics.json, test_run.json.")


if __name__ == "__main__":
    main()
