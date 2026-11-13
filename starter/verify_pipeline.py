"""Đo bổ sung và kiểm thử pipeline trong thư mục/schema riêng, giữ nguyên baseline."""
import copy
import hashlib
import importlib.metadata
import importlib.util
import io
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from contextlib import redirect_stdout
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

import pg8000.native

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
RESULTS = BASE / "results"
MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def baseline_hashes():
    frozen = read(RESULTS / "selection.json")["frozen_sha256"]
    for name, expected in frozen.items():
        if sha(ROOT / name.replace("\\", "/")) != expected:
            raise ValueError(f"Baseline thay đổi: {name}")
    return {name: sha(RESULTS / name) for name in (
        "selection.json", "dev_metrics.json", "dev_traces.json", "dev_run.json",
        "test_metrics.json", "test_traces.json", "test_run.json")}


def connect():
    return pg8000.native.Connection(user="day6", password="day6_local_only",
             host="127.0.0.1", port=55433, database="day6_lab", timeout=10)


def database_digest(connection, table="public.chunks"):
    # table chỉ do script chỉ định, không nhận giá trị từ người dùng.
    rows = connection.run("SELECT strategy, chunk_id, document_id, source, page, chapter, content, embedding::text FROM " + table + " ORDER BY strategy, chunk_id")
    return hashlib.sha256(json.dumps(rows, ensure_ascii=False).encode()).hexdigest()


def import_script(name):
    spec = importlib.util.spec_from_file_location(name, BASE / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    before = baseline_hashes()
    RESULT = {
        "measured_at": datetime.now(timezone.utc).isoformat(),
        "scope": "Supplementary profiling/verification after holdout evaluation; original dev/test unchanged.",
        "baseline_hashes_before": before,
        "versions": {"python": platform.python_version(), **{
            name: importlib.metadata.version(name) for name in
            ("pypdf", "fonttools", "sentence-transformers", "torch", "transformers", "pg8000")}},
        "source_scripts_sha256": {name: sha(BASE / name) for name in
            ("read_pdf.py", "chunk_pages.py", "chunk_sections.py", "load_database.py", "search.py", "embed_chunks.py")},
        "checks": [], "timings": {},
        "timing_limits": "One supplementary warm-cache CPU run; subprocess startup included in extraction/chunk timings. Model load, document encode and DB ingest measured separately. No peak RAM, electricity or hardware cost measured.",
        "api_cost_usd": 0
    }

    def check(name, condition, detail):
        if not condition:
            raise AssertionError(name + ": " + detail)
        RESULT["checks"].append({"name": name, "passed": True, "detail": detail})

    # Chạy đúng các script gốc, nhưng output chỉ vào thư mục tạm.
    with tempfile.TemporaryDirectory(prefix="day06_verify_") as temp:
        work = Path(temp)
        (work / "data").mkdir()
        shutil.copyfile(BASE / "data/thinkpython2.pdf", work / "data/thinkpython2.pdf")
        stage_outputs = {"read_pdf.py": "pages.json", "chunk_pages.py": "chunks_A.json", "chunk_sections.py": "chunks_B.json"}
        for script, output in stage_outputs.items():
            shutil.copyfile(BASE / script, work / script)
            started = time.perf_counter()
            run = subprocess.run([sys.executable, str(work / script)], cwd=work,
                     env={**os.environ, "PYTHONIOENCODING": "utf-8"}, capture_output=True, text=True, encoding="utf-8")
            RESULT["timings"][script] = {"seconds": time.perf_counter() - started,
                         "stdout": run.stdout, "stderr": run.stderr, "returncode": run.returncode}
            check(script + " completes", run.returncode == 0, run.stderr or "Script completed")
            check(script + " matches baseline", read(work / "data" / output) == read(BASE / "data" / output), "Generated JSON equals the original artifact")

        # Đo model snapshot được chỉ định bằng SHA, chỉ đọc cache có sẵn.
        cache = Path(os.environ.get("HF_HUB_CACHE", str(Path.home() / ".cache/huggingface/hub"))) / "models--sentence-transformers--all-MiniLM-L6-v2"
        revision = (cache / "refs/main").read_text(encoding="utf-8").strip()
        if not re.fullmatch(r"[a-f0-9]{40}", revision):
            raise ValueError("Invalid model revision in local cache")
        snapshot = cache / "snapshots" / revision
        file_hashes = {p.relative_to(snapshot).as_posix(): sha(p) for p in sorted(snapshot.rglob("*")) if p.is_file()}
        RESULT["model_snapshot"] = {"model": MODEL, "revision": revision,
             "files_sha256": file_hashes, "recorded_at": RESULT["measured_at"],
             "historical_note": "Snapshot inspected after test; original dev/test run did not record a revision. Re-encoding below tests numerical agreement with stored document vectors."}
        from sentence_transformers import SentenceTransformer
        started = time.perf_counter()
        model = SentenceTransformer(MODEL, revision=revision, device="cpu", local_files_only=True)
        RESULT["timings"]["cached_model_load_seconds"] = time.perf_counter() - started
        RESULT["model_snapshot"]["max_seq_length"] = model.max_seq_length
        RESULT["model_snapshot"]["dimensions"] = model.get_sentence_embedding_dimension()
        encoded = {}
        for strategy in ("A", "B"):
            chunks = read(BASE / f"data/chunks_{strategy}_embedded.json")
            texts = [c["text"] for c in chunks]
            lengths = [len(ids) for ids in model.tokenizer(texts, truncation=False)["input_ids"]]
            started = time.perf_counter()
            vectors = model.encode(texts, batch_size=16, normalize_embeddings=True,
                                  show_progress_bar=True).tolist()
            elapsed = time.perf_counter() - started
            maximum_delta = max(abs(a - b) for c, v in zip(chunks, vectors) for a, b in zip(c["embedding"], v))
            check(strategy + " pinned model agrees with stored vectors", maximum_delta <= 1e-5,
                  f"Maximum absolute difference {maximum_delta:.9g}; tolerance 1e-5")
            RESULT["timings"]["document_embedding_" + strategy] = {
                "seconds": elapsed, "chunks": len(chunks), "tokens_before_truncation": sum(lengths),
                "over_limit": sum(n > model.max_seq_length for n in lengths),
                "max_absolute_difference_from_original": maximum_delta,
                "note": "Reproduces the existing truncation behavior; not a corrected retrieval experiment."}
            encoded[strategy] = chunks

        # Kiểm tra dữ liệu lỗi phải bị từ chối, không tạo vector giả.
        loader = import_script("load_database")
        invalid_dir = work / "invalid"
        invalid_dir.mkdir()
        invalid_path = invalid_dir / "chunks_A_embedded.json"
        for label, change in (
            ("reject wrong vector dimensions", lambda c: c[0].update(embedding=[1.0])),
            ("reject duplicate IDs", lambda c: c.append(copy.deepcopy(c[0]))),
            ("reject wrong chapter", lambda c: c[0].update(chapter=12)),
            ("reject empty document text", lambda c: c[0].update(text=" ")),
        ):
            bad = copy.deepcopy(encoded["A"][:2])
            change(bad)
            save(invalid_path, bad)
            rejected = False
            with patch.object(loader, "DATA_DIR", invalid_dir):
                try:
                    loader.read_chunks("A")
                except ValueError:
                    rejected = True
            check(label, rejected, "Invalid input rejected before database writes")

        # Dùng schema riêng và chính loader gốc; không nạp vào public.chunks.
        schema = "day06_verification_" + uuid.uuid4().hex[:12]
        quoted = pg8000.native.identifier(schema)
        original_connect = pg8000.native.Connection
        admin = connect()
        public_before = database_digest(admin)
        try:
            admin.run("CREATE SCHEMA " + quoted)
            admin.run("CREATE TABLE " + quoted + ".chunks (LIKE public.chunks INCLUDING ALL)")

            def isolated_connection(*args, **kwargs):
                con = original_connect(*args, **kwargs)
                con.run("SET search_path TO " + quoted + ", public")
                return con

            def isolated_load(datasets=None):
                start = time.perf_counter()
                with patch.object(pg8000.native, "Connection", isolated_connection):
                    with redirect_stdout(io.StringIO()):
                        if datasets is None:
                            loader.main()
                        else:
                            with patch.object(loader, "read_chunks", lambda s: copy.deepcopy(datasets[s])):
                                loader.main()
                return time.perf_counter() - start

            for run_id in ("first_ingestion", "repeat_ingestion"):
                elapsed = isolated_load()
                counts = admin.run("SELECT strategy, COUNT(*) FROM " + quoted + ".chunks GROUP BY strategy ORDER BY strategy")
                check(run_id + " counts", counts == [["A", 151], ["B", 104]], str(counts))
                RESULT["timings"][run_id] = {"seconds": elapsed,
                    "scope": "Same loader and real 255 vectors; isolated table; includes validation, connection, upsert, prune and commit"}
            check("repeat ingestion content unchanged", database_digest(admin, quoted + ".chunks") == public_before,
                  "All IDs, metadata, text and vectors equal original 255-row snapshot after two loads")

            changed = copy.deepcopy(encoded)
            changed["B"] = changed["B"][:-1]
            changed["B"][0]["text"] = "Verification-only document update.\n" + changed["B"][0]["text"]
            changed["B"][0]["embedding"] = model.encode(changed["B"][0]["text"], normalize_embeddings=True).tolist()
            isolated_load(changed)
            counts = admin.run("SELECT strategy, COUNT(*) FROM " + quoted + ".chunks GROUP BY strategy ORDER BY strategy")
            content = admin.run("SELECT content FROM " + quoted + ".chunks WHERE strategy='B' AND chunk_id=:id", id=changed["B"][0]["chunk_id"])[0][0]
            stale = admin.run("SELECT COUNT(*) FROM " + quoted + ".chunks WHERE strategy='B' AND chunk_id=:id", id=encoded["B"][-1]["chunk_id"])[0][0]
            stored_vector = json.loads(admin.run("SELECT embedding::text FROM " + quoted + ".chunks WHERE strategy='B' AND chunk_id=:id", id=changed["B"][0]["chunk_id"])[0][0])
            vector_updated = max(abs(a-b) for a,b in zip(stored_vector, changed["B"][0]["embedding"])) < 1e-6
            vector_changed = max(abs(a-b) for a,b in zip(stored_vector, encoded["B"][0]["embedding"])) > 1e-4
            check("updated document replaces text/vector and prunes obsolete chunks", counts == [["A", 151], ["B", 103]] and content == changed["B"][0]["text"] and stale == 0 and vector_updated and vector_changed,
                  "B has 103 rows, changed text and newly encoded vector updated, deleted ID absent; A unchanged")

            previous = database_digest(admin, quoted + ".chunks")
            broken = copy.deepcopy(changed)
            broken["A"][0]["text"] += "\nThis change must be rolled back."
            broken["B"][0]["embedding"] = [1.0]
            failed = False
            try:
                isolated_load(broken)
            except pg8000.native.DatabaseError:
                failed = True
            check("SQL failure rolls back complete transaction", failed and database_digest(admin, quoted + ".chunks") == previous,
                  "Deliberately invalid vector caused database error; previous A/B content unchanged")
            isolated_load()

            search = import_script("search")
            with patch.object(pg8000.native, "Connection", isolated_connection):
                vector = encoded["A"][0]["embedding"]
                hits = search.search_chunks(vector, "A")
                check("cosine self match", len(hits) == 3 and abs(hits[0]["distance"]) < 1e-5, "Known real document vector has top distance near zero")
                filtered = search.search_chunks(vector, "C", 12)
                check("SQL chapter filter", len(filtered) == 3 and all(h["chapter"] == 12 for h in filtered), "All C results satisfy chapter=12 even for a query vector from chapter 10")
                b = search.search_chunks(vector, "B")
                c = search.search_chunks(vector, "C")
                check("C without filter equals B", b == c, "Identical top-3 IDs, scores and metadata")
        finally:
            # Xóa đúng schema ngẫu nhiên script này tạo, không xóa dữ liệu bài làm.
            admin.run("DROP SCHEMA IF EXISTS " + quoted + " CASCADE")
            public_after = database_digest(admin)
            admin.close()
        check("production database unchanged", public_before == public_after, "Hash of public.chunks unchanged")
        RESULT["database_sha256_before"] = public_before
        RESULT["database_sha256_after"] = public_after

    after = baseline_hashes()
    check("frozen dev/test unchanged", before == after, "Original selection, metrics, traces, model inputs and code hashes unchanged")
    RESULT["baseline_hashes_after"] = after
    RESULT["passed"] = True
    save(RESULTS / "supplementary_verification.json", RESULT)
    model_lock = RESULT["model_snapshot"]
    save(BASE / "model_snapshot.json", model_lock)
    lines = ["# Kiểm thử và đo bổ sung", "", "Các phép đo được thực hiện sau lần test gốc; không thay thế thời gian của lần chạy ban đầu.", "",
             "## Thời gian", "", "| Giai đoạn | Giây |", "|---|---:|"]
    for name, value in RESULT["timings"].items():
        seconds = value["seconds"] if isinstance(value, dict) else value
        lines.append(f"| {name} | {seconds:.4f} |")
    lines += ["", "## Kiểm thử", ""]
    for item in RESULT["checks"]:
        lines += [f"- PASS — {item['name']}: {item['detail']}"]
    lines += ["", "## Model", "", f"Snapshot kiểm tra: `{MODEL}@{model_lock['revision']}`.",
              "Các file model được ghi SHA-256. Vector tái tạo được so với vector cũ, dung sai tuyệt đối 1e-5.", "",
              "## Giới hạn", "", RESULT["timing_limits"],
              "B/C vẫn giữ giới hạn token của thí nghiệm gốc trong phép đo này. Không chạy lại câu hỏi test hoặc tạo điểm retrieval mới.", ""]
    (RESULTS / "supplementary_verification.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"PASS: {len(RESULT['checks'])} checks. Original database and dev/test artifacts unchanged.", flush=True)
    print("Saved supplementary_verification.json/.md and model_snapshot.json", flush=True)


if __name__ == "__main__":
    RESULTS.mkdir(exist_ok=True)
    try:
        main()
    except Exception as exc:
        with (RESULTS / "verification_errors.jsonl").open("a", encoding="utf-8") as stream:
            stream.write(json.dumps({"time": datetime.now(timezone.utc).isoformat(),
                                    "type": type(exc).__name__, "message": str(exc)}, ensure_ascii=False) + "\n")
        raise
