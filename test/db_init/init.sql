-- Enable the pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create the schema
CREATE TABLE professors (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE papers (
    id SERIAL PRIMARY KEY,
    professor_id INT NOT NULL,
    title TEXT NOT NULL,
    abstract TEXT,
    embedding VECTOR(384), -- Vector type for 384-dimensional embeddings
    paper_link TEXT,
    FOREIGN KEY (professor_id) REFERENCES professors(id) ON DELETE CASCADE
);

-- Create an index for efficient nearest neighbor search on embeddings
CREATE INDEX papers_embedding_idx ON papers USING ivfflat (embedding) WITH (lists = 100);
