CREATE DATABASE IF NOT EXISTS cs_research_db;
USE cs_research_db;

CREATE TABLE IF NOT EXISTS papers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    authors TEXT,
    publication_date DATE,
    journal VARCHAR(255),
    abstract TEXT,
    url VARCHAR(255),
    keywords TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_papers_title ON papers(title);
CREATE INDEX idx_papers_keywords ON papers(keywords);

-- Metadata
CREATE TABLE IF NOT EXISTS config (
    id INT AUTO_INCREMENT PRIMARY KEY,
    key VARCHAR(255) UNIQUE NOT NULL,
    value TEXT
);

INSERT INTO config (key, value) VALUES
('version', '1.0'),
('last_updated', NOW());