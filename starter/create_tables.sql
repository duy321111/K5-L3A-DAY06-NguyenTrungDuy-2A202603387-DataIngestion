-- GUIDE.md, section 3: persistent vector storage for strategies A and B.
CREATE TABLE IF NOT EXISTS chunks (
    strategy TEXT NOT NULL,
    chunk_id TEXT NOT NULL,
    document_id TEXT NOT NULL,
    source TEXT NOT NULL,
    page INTEGER NOT NULL,
    chapter INTEGER NOT NULL,
    content TEXT NOT NULL,
    embedding VECTOR(384) NOT NULL,

    PRIMARY KEY (strategy, chunk_id)
);
