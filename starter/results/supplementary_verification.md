# Kiểm thử và đo bổ sung

Các phép đo được thực hiện sau lần test gốc; không thay thế thời gian của lần chạy ban đầu.

## Thời gian

| Giai đoạn | Giây |
|---|---:|
| read_pdf.py | 1.0750 |
| chunk_pages.py | 0.0806 |
| chunk_sections.py | 0.0867 |
| cached_model_load_seconds | 1.7246 |
| document_embedding_A | 5.6764 |
| document_embedding_B | 4.6433 |
| first_ingestion | 2.9546 |
| repeat_ingestion | 2.8546 |

## Kiểm thử

- PASS — read_pdf.py completes: Script completed
- PASS — read_pdf.py matches baseline: Generated JSON equals the original artifact
- PASS — chunk_pages.py completes: Script completed
- PASS — chunk_pages.py matches baseline: Generated JSON equals the original artifact
- PASS — chunk_sections.py completes: Script completed
- PASS — chunk_sections.py matches baseline: Generated JSON equals the original artifact
- PASS — A pinned model agrees with stored vectors: Maximum absolute difference 0; tolerance 1e-5
- PASS — B pinned model agrees with stored vectors: Maximum absolute difference 0; tolerance 1e-5
- PASS — reject wrong vector dimensions: Invalid input rejected before database writes
- PASS — reject duplicate IDs: Invalid input rejected before database writes
- PASS — reject wrong chapter: Invalid input rejected before database writes
- PASS — reject empty document text: Invalid input rejected before database writes
- PASS — first_ingestion counts: [['A', 151], ['B', 104]]
- PASS — repeat_ingestion counts: [['A', 151], ['B', 104]]
- PASS — repeat ingestion content unchanged: All IDs, metadata, text and vectors equal original 255-row snapshot after two loads
- PASS — updated document replaces text/vector and prunes obsolete chunks: B has 103 rows, changed text and newly encoded vector updated, deleted ID absent; A unchanged
- PASS — SQL failure rolls back complete transaction: Deliberately invalid vector caused database error; previous A/B content unchanged
- PASS — cosine self match: Known real document vector has top distance near zero
- PASS — SQL chapter filter: All C results satisfy chapter=12 even for a query vector from chapter 10
- PASS — C without filter equals B: Identical top-3 IDs, scores and metadata
- PASS — production database unchanged: Hash of public.chunks unchanged
- PASS — frozen dev/test unchanged: Original selection, metrics, traces, model inputs and code hashes unchanged

## Model

Snapshot kiểm tra: `sentence-transformers/all-MiniLM-L6-v2@1110a243fdf4706b3f48f1d95db1a4f5529b4d41`.
Các file model được ghi SHA-256. Vector tái tạo được so với vector cũ, dung sai tuyệt đối 1e-5.

## Giới hạn

One supplementary warm-cache CPU run; subprocess startup included in extraction/chunk timings. Model load, document encode and DB ingest measured separately. No peak RAM, electricity or hardware cost measured.
B/C vẫn giữ giới hạn token của thí nghiệm gốc trong phép đo này. Không chạy lại câu hỏi test hoặc tạo điểm retrieval mới.
