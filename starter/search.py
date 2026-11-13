"""GUIDE.md, mục 3: tìm top-3 bằng cosine trong PostgreSQL + pgvector."""
import argparse
import json
import math

import pg8000.native

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def search_chunks(query_vector, strategy="A", chapter=None):
    """Database xếp hạng vector; chỉ C được áp dụng bộ lọc chương."""
    if strategy not in {"A", "B", "C"}:
        raise ValueError("Cấu hình phải là A, B hoặc C.")
    if chapter is not None and (strategy != "C" or chapter not in (10, 11, 12)):
        raise ValueError("Lọc chương 10/11/12 chỉ áp dụng cho cấu hình C.")
    if len(query_vector) != 384 or not all(
        type(v) in (int, float) and math.isfinite(v) for v in query_vector
    ) or not any(v != 0 for v in query_vector):
        raise ValueError("Vector câu hỏi phải có 384 số hữu hạn và không được toàn số 0.")

    # C dùng chính các chunk/vector của B, chỉ thay điều kiện lọc.
    stored_strategy = "B" if strategy == "C" else strategy
    parameters = {
        "strategy": stored_strategy,
        "query_vector": json.dumps(query_vector, allow_nan=False)
    }
    filter_sql = ""
    if chapter is not None:
        filter_sql = " AND chapter = :chapter"
        parameters["chapter"] = chapter

    connection = pg8000.native.Connection(
        user="day6",
        password="day6_local_only",
        host="127.0.0.1",
        port=55433,
        database="day6_lab",
        timeout=10
    )
    try:
        count = connection.run(
            "SELECT COUNT(*) FROM chunks WHERE strategy = :strategy",
            strategy=stored_strategy
        )[0][0]
        if count == 0:
            raise RuntimeError("Chưa có dữ liệu. Hãy chạy python load_database.py trước.")

        # <=> là cosine distance: càng nhỏ thì vector càng gần nhau.
        # SQL được ghép từ đoạn cố định; giá trị người dùng truyền bằng tham số.
        rows = connection.run(
            """
            SELECT chunk_id, document_id, source, page, chapter, content,
                   embedding <=> CAST(:query_vector AS vector) AS distance
            FROM chunks
            WHERE strategy = :strategy
            """ + filter_sql + """
            ORDER BY distance ASC, chunk_id ASC
            LIMIT 3
            """,
            **parameters
        )
    finally:
        connection.close()

    return [
        {
            "chunk_id": row[0],
            "document_id": row[1],
            "source": row[2],
            "page": row[3],
            "chapter": row[4],
            "text": row[5],
            "distance": float(row[6]),
            "score": 1 - float(row[6])
        }
        for row in rows
    ]


def main():
    parser = argparse.ArgumentParser(description="Tìm 3 đoạn liên quan nhất trong sách Think Python.")
    parser.add_argument("--question", help="Câu hỏi bằng tiếng Anh; bỏ trống để nhập khi chạy.")
    parser.add_argument("--strategy", choices=["A", "B", "C"], default="A")
    parser.add_argument("--chapter", type=int, choices=[10, 11, 12])
    args = parser.parse_args()

    if args.chapter is not None and args.strategy != "C":
        parser.error("--chapter chỉ dùng cùng --strategy C")
    question = args.question if args.question is not None else input("Nhập câu hỏi tiếng Anh: ")
    question = question.strip()
    if not question:
        parser.error("Câu hỏi không được rỗng.")

    # Dùng cùng model và cách chuẩn hóa với embed_chunks.py.
    from sentence_transformers import SentenceTransformer
    print("Đang nạp model...", flush=True)
    model = SentenceTransformer(MODEL_NAME)
    token_count = len(model.tokenizer(question, truncation=False)["input_ids"])
    if token_count > model.max_seq_length:
        parser.error(f"Câu hỏi quá dài: tối đa {model.max_seq_length} token.")
    query_vector = model.encode(question, normalize_embeddings=True).tolist()

    hits = search_chunks(query_vector, args.strategy, args.chapter)
    print(f"\nCấu hình {args.strategy} — tìm được {len(hits)} đoạn:")
    for rank, hit in enumerate(hits, 1):
        print(f"\n--- Kết quả {rank} ---")
        print(f"Chunk: {hit['chunk_id']}")
        print(f"Trang PDF: {hit['page']} | Chương: {hit['chapter']}")
        print(f"Điểm tương đồng cosine: {hit['score']:.4f}")
        print("Nguồn:", hit["source"])
        print(hit["text"])
    if not hits:
        print("Không có đoạn nào phù hợp với điều kiện lọc.")


if __name__ == "__main__":
    main()
