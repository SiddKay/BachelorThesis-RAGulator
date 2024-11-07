-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create custom types
CREATE TYPE score_value AS ENUM ('0', '1', '2', '3', '4', '5');

-- Evaluation Sessions
CREATE TABLE evaluation_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    chain_id UUID NOT NULL REFERENCES chains(id),
    question_set_id UUID NOT NULL REFERENCES question_sets(id),
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_session_name UNIQUE (name)
);

CREATE INDEX idx_evaluation_sessions_chain_id ON evaluation_sessions(chain_id);
CREATE INDEX idx_evaluation_sessions_question_set_id ON evaluation_sessions(question_set_id);

COMMENT ON TABLE evaluation_sessions IS 'Tracks evaluation sessions for specific chains and question sets';


-- Chain table
CREATE TABLE chains (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(512) NOT NULL,
    CONSTRAINT unique_file_path UNIQUE (file_path)
);

COMMENT ON TABLE chains IS 'Stores information about LangChain chain files available for evaluation';
COMMENT ON COLUMN chains.file_name IS 'Name of the chain file';
COMMENT ON COLUMN chains.file_path IS 'Path to the chain file in the backend directory';

-- Question Sets
CREATE TABLE question_sets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_question_set_name UNIQUE (name)
);

CREATE INDEX idx_question_sets_name ON question_sets(name);

COMMENT ON TABLE question_sets IS 'Collection of questions used for evaluating chain performance';

-- Questions
CREATE TABLE questions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    question_set_id UUID NOT NULL REFERENCES question_sets(id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    expected_answer TEXT,
    sequence_number INTEGER NOT NULL,
    important BOOLEAN DEFAULT false,
    CONSTRAINT unique_question_in_set UNIQUE (question_set_id, sequence_number)
);

CREATE INDEX idx_questions_question_set_id ON questions(question_set_id);

COMMENT ON TABLE questions IS 'Individual questions within question sets';

-- Config Versions
CREATE TABLE config_versions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES evaluation_sessions(id) ON DELETE CASCADE,
    model_parameters JSONB NOT NULL DEFAULT '{}',
    prompt_template TEXT,
    version_label VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_version_label_per_session UNIQUE (session_id, version_label)
);

CREATE INDEX idx_config_versions_session_id ON config_versions(session_id);
CREATE INDEX idx_config_versions_model_parameters ON config_versions USING gin (model_parameters);

COMMENT ON TABLE config_versions IS 'Stores different configurations used in evaluation sessions';

-- Answers
CREATE TABLE answers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    question_id UUID NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    config_version_id UUID NOT NULL REFERENCES config_versions(id) ON DELETE CASCADE,
    generated_answer TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_answer_per_config UNIQUE (question_id, config_version_id)
);

CREATE INDEX idx_answers_question_id ON answers(question_id);
CREATE INDEX idx_answers_config_version_id ON answers(config_version_id);

COMMENT ON TABLE answers IS 'Stores generated answers for questions under specific configurations';

-- Comments
CREATE TABLE comments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    answer_id UUID NOT NULL REFERENCES answers(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_comments_answer_id ON comments(answer_id);

COMMENT ON TABLE comments IS 'User comments on generated answers';

-- Scores
CREATE TABLE scores (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    answer_id UUID NOT NULL REFERENCES answers(id) ON DELETE CASCADE,
    value score_value NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_score_per_answer UNIQUE (answer_id)
);

CREATE INDEX idx_scores_answer_id ON scores(answer_id);

COMMENT ON TABLE scores IS 'User scores for generated answers';

-- Triggers for updated_at timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_question_sets_updated_at
    BEFORE UPDATE ON question_sets
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_evaluation_sessions_updated_at
    BEFORE UPDATE ON evaluation_sessions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Add helpful views for common queries
CREATE VIEW v_evaluation_summary AS
SELECT 
    es.id as session_id,
    es.name as session_name,
    c.file_name as chain_name,
    qs.name as question_set_name,
    COUNT(DISTINCT cv.id) as config_versions_count,
    COUNT(DISTINCT a.id) as total_answers,
    AVG(
        CASE s.value
            WHEN '0' THEN 0
            WHEN '1' THEN 1
            WHEN '2' THEN 2
            WHEN '3' THEN 3
            WHEN '4' THEN 4
            WHEN '5' THEN 5
        END
    ) as average_score
FROM evaluation_sessions es
JOIN chains c ON es.chain_id = c.id
JOIN question_sets qs ON es.question_set_id = qs.id
LEFT JOIN config_versions cv ON es.id = cv.session_id
LEFT JOIN answers a ON cv.id = a.config_version_id
LEFT JOIN scores s ON a.id = s.answer_id
GROUP BY es.id, es.name, c.file_name, qs.name;

COMMENT ON VIEW v_evaluation_summary IS 'Provides summary statistics for evaluation sessions';