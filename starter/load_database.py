"""GUIDE.md, mục 3: nạp chunk và embedding thật từ JSON vào pgvector."""
import json
import math
from pathlib import Path

import pg8000.native

DATA_DIR = Path(__file__).parent / "data"
DOCUMENT_ID = "thinkpython2"
DIMENSIONS = 384


def read_chunks(strategy):
    """Kiểm tra toàn bộ file trước khi thay đổi database."""
    path = DATA_DIR / f"chunks_{strategy}_embedded.json"
    chunks = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(chunks, list) or not chunks:
        raise ValueError(f"{path.name}: danh sách chunk bị rỗng hoặc sai định dạng.")

    seen_ids = set()
    for chunk in chunks:
        required = {"chunk_id", "document_id", "source", "page", "chapter", "text", "embedding"}
        if not isinstance(chunk, dict) or not required.issubset(chunk):
            raise ValueError(f"{path.name}: chunk thiếu trường bắt buộc.")

        chunk_id = chunk["chunk_id"]
        if not isinstance(chunk_id, str) or not chunk_id.strip() or chunk_id in seen_ids:
            raise ValueError(f"{path.name}: chunk_id rỗng hoặc trùng.")
        seen_ids.add(chunk_id)

        if chunk["document_id"] != DOCUMENT_ID:
            raise ValueError(f"{chunk_id}: document_id không đúng tài liệu đang nạp.")
        for field in ("source", "text"):
            if not isinstance(chunk[field], str) or not chunk[field].strip():
                raise ValueError(f"{chunk_id}: {field} không được rỗng.")
        if type(chunk["page"]) is not int or not 111 <= chunk["page"] <= 146:
            raise ValueError(f"{chunk_id}: số trang phải nằm trong 111–146.")
        expected_chapter = 10 if chunk["page"] <= 124 else 11 if chunk["page"] <= 136 else 12
        if type(chunk["chapter"]) is not int or chunk["chapter"] != expected_chapter:
            raise ValueError(f"{chunk_id}: chương không khớp số trang.")

        vector = chunk["embedding"]
        if not isinstance(vector, list) or len(vector) != DIMENSIONS:
            raise ValueError(f"{chunk_id}: embedding phải gồm {DIMENSIONS} số.")
        if not all(type(v) in (int, float) and math.isfinite(v) for v in vector):
            raise ValueError(f"{chunk_id}: vector có giá trị không hợp lệ.")
        if not any(v != 0 for v in vector):
            raise ValueError(f"{chunk_id}: vector không được toàn số 0.")

    return chunks


def main():
    # 1. Đọc và kiểm tra cả A/B trước khi kết nối database.
    datasets = {strategy: read_chunks(strategy) for strategy in ("A", "B")}

    # 2. Kết nối PostgreSQL local đang chạy trong Docker.
    connection = pg8000.native.Connection(
        user="day6",
        password="day6_local_only",
        host="127.0.0.1",
        port=55433,
        database="day6_lab",
        timeout=10
    )

    counts = {}
    try:
        # Transaction: nếu bất kỳ bước nào lỗi, hoàn tác cả lần nạp.
        connection.run("START TRANSACTION")
        try:
            for strategy, chunks in datasets.items():
                for chunk in chunks:
                    # Tham số được truyền riêng, không ghép nội dung vào câu SQL.
                    # Trùng khóa chính thì cập nhật, không tạo thêm dòng.
                    connection.run(
                        """
                        INSERT INTO chunks (
                            strategy, chunk_id, document_id, source,
                            page, chapter, content, embedding
                        ) VALUES (
                            :strategy, :chunk_id, :document_id, :source,
                            :page, :chapter, :content, CAST(:embedding AS vector)
                        )
                        ON CONFLICT (strategy, chunk_id) DO UPDATE SET
                            document_id = EXCLUDED.document_id,
                            source = EXCLUDED.source,
                            page = EXCLUDED.page,
                            chapter = EXCLUDED.chapter,
                            content = EXCLUDED.content,
                            embedding = EXCLUDED.embedding
                        """,
                        strategy=strategy,
                        chunk_id=chunk["chunk_id"],
                        document_id=chunk["document_id"],
                        source=chunk["source"],
                        page=chunk["page"],
                        chapter=chunk["chapter"],
                        content=chunk["text"],
                        embedding=json.dumps(chunk["embedding"], allow_nan=False)
                    )

                # 3. Xóa chunk cũ của đúng tài liệu/cấu hình nếu JSON đã thay đổi.
                connection.run(
                    """
                    DELETE FROM chunks
                    WHERE strategy = :strategy AND document_id = :document_id
                      AND NOT (chunk_id = ANY(CAST(:chunk_ids AS text[])))
                    """,
                    strategy=strategy,
                    document_id=DOCUMENT_ID,
                    chunk_ids=[chunk["chunk_id"] for chunk in chunks]
                )

                count = connection.run(
                    """
                    SELECT COUNT(*) FROM chunks
                    WHERE strategy = :strategy AND document_id = :document_id
                    """,
                    strategy=strategy,
                    document_id=DOCUMENT_ID
                )[0][0]
                if count != len(chunks):
                    raise RuntimeError(f"Cấu hình {strategy}: số dòng sau khi nạp không khớp JSON.")
                counts[strategy] = count

            connection.run("COMMIT")
        except Exception:
            connection.run("ROLLBACK")
            raise
    finally:
        connection.close()

    for strategy, count in counts.items():
        print(f"Cấu hình {strategy}: đã lưu {count} chunk vào PostgreSQL.")
    print("Hoàn tất. Chạy lại sẽ cập nhật dữ liệu, không tạo chunk trùng.")


if __name__ == "__main__":
    main()
