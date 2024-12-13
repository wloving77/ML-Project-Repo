CREATE DATABASE IF NOT EXISTS cs_research_vectordb;
\c cs_research_vectordb;

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS embeddings (
    id SERIAL PRIMARY KEY,
    paper_id INT REFERENCES ml_team.papers(id) ON DELETE CASCADE,  
    vector vector(1536),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_embeddings_vector ON embeddings USING ivfflat (vector);
