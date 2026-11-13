"""Tạo chunk không vượt giới hạn token cho thí nghiệm sau; không sửa baseline."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

BASE=Path(__file__).resolve().parent


def split_text(text, tokenizer, limit):
    """Giữ nguyên toàn bộ ký tự và ưu tiên cắt tại khoảng trắng."""
    if limit < 8:
        raise ValueError("Token limit must be >=8")
    pieces=[]
    start=0
    while start < len(text):
        if len(tokenizer(text[start:], truncation=False)["input_ids"]) <= limit:
            pieces.append(text[start:])
            break
        low, high = start+1, len(text)
        best=start
        while low <= high:
            end=(low+high)//2
            if len(tokenizer(text[start:end],truncation=False)["input_ids"]) <= limit:
                best=end
                low=end+1
            else:
                high=end-1
        if best==start:
            raise ValueError("Cannot fit even one character within token limit")
        boundary=max(text.rfind("\n",start,best),text.rfind(" ",start,best))
        if boundary > start+(best-start)//2:
            best=boundary+1
        # Tokenizer có thể đổi cách tách ở ranh giới từ; luôn xác nhận lại.
        while best > start and len(tokenizer(text[start:best],truncation=False)["input_ids"]) > limit:
            best-=1
        if best==start:
            raise ValueError("Cannot find a valid token boundary")
        pieces.append(text[start:best])
        start=best
    if "".join(pieces)!=text:
        raise AssertionError("Text content changed while splitting")
    return pieces


def main():
    lock=json.loads((BASE/"model_snapshot.json").read_text(encoding="utf-8"))
    from transformers import AutoTokenizer
    tokenizer=AutoTokenizer.from_pretrained(lock["model"],revision=lock["revision"],local_files_only=True)
    limit=lock["max_seq_length"]
    output=BASE/"results/token_safe"
    output.mkdir(exist_ok=True)
    summary={"created_at":datetime.now(timezone.utc).isoformat(),"model":lock["model"],
             "revision":lock["revision"],"token_limit":limit,
             "purpose":"Preparation for a future experiment after viewing the old test. No new retrieval scores or claims of independent test evaluation.",
             "strategies":[]}
    for strategy in ("A","B"):
        path=BASE/f"data/chunks_{strategy}.json"
        chunks=json.loads(path.read_text(encoding="utf-8"))
        rows=[]
        split_count=0
        for chunk in chunks:
            parts=split_text(chunk["text"],tokenizer,limit)
            split_count+=len(parts)>1
            start=0
            for i,text in enumerate(parts):
                count=len(tokenizer(text,truncation=False)["input_ids"])
                if count>limit:
                    raise AssertionError("Overlength token-safe chunk")
                rows.append({**chunk,"chunk_id":f"{chunk['chunk_id']}__tokenpart{i}",
                             "parent_chunk_id":chunk["chunk_id"],"text":text,
                             "parent_char_start":start,"parent_char_end":start+len(text),
                             "token_count":count})
                start+=len(text)
        if len({r["chunk_id"] for r in rows})!=len(rows):
            raise AssertionError("Duplicate token-safe IDs")
        destination=output/f"chunks_{strategy}.json"
        destination.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        summary["strategies"].append({"strategy":strategy,"original_chunks":len(chunks),
            "chunks_split":split_count,"token_safe_chunks":len(rows),
            "maximum_tokens":max(r["token_count"] for r in rows),"over_limit":0,
            "all_characters_preserved":True,"original_sha256":hashlib.sha256(path.read_bytes()).hexdigest()})
    # C của thí nghiệm sau sẽ dùng chung B; chưa nạp hay đánh giá các chunk mới.
    (output/"summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary["strategies"],ensure_ascii=False,indent=2))
    print("Baseline không đổi. Chưa tạo embedding, nạp database hay chạy retrieval cho bộ chunk mới.")


if __name__=="__main__":
    main()
