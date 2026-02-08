CREATE TABLE IF NOT EXISTS feedback_logs (
    id SERIAL PRIMARY KEY,
    menu_id INT NOT NULL,
    sentiment FLOAT,
    tags TEXT [],
    confidence FLOAT,
    raw_text TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public';
ALTER TABLE ai_interactions
ADD COLUMN model_name TEXT;
select *
from ai_interactions;