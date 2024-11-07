-- Enable UUID extension for PostgreSQL
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create custom types
CREATE TYPE score_range AS ENUM ('0', '1', '2', '3', '4', '5');

-- Sessions table
-- Stores evaluation sessions which can contain multiple chain evaluations
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    last_accessed TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexes
    CONSTRAINT sessions_name_unique UNIQUE (name)
);

-- Chains table
-- Represents LangChain expression chains imported from files
CREATE TABLE chains (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    file_name VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    imported_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT chains_file_path_unique UNIQUE (file_path),
    CONSTRAINT chains_file_name_unique UNIQUE (file_name)
);

-- Questions table
-- Stores questions and expected answers for evaluation sessions
CREATE TABLE questions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL,
    question_text TEXT NOT NULL,
    expected_answer TEXT,
    sequence_number INTEGER NOT NULL,
    
    -- Foreign Keys
    CONSTRAINT fk_questions_session
        FOREIGN KEY (session_id)
        REFERENCES sessions(id)
        ON DELETE CASCADE,
    
    -- Constraints
    CONSTRAINT questions_sequence_session_unique 
        UNIQUE (session_id, sequence_number)
);

-- Configurations table
-- Stores chain configurations including prompt templates and model parameters
CREATE TABLE configurations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    prompt_template JSONB,
    model_params JSONB,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexes
    -- Add GIN index for faster JSONB querying if needed
    -- Commented out by default - uncomment if query patterns show it's necessary
    -- CREATE INDEX idx_configurations_model_params ON configurations USING GIN (model_params);
    
    -- Constraints
    CONSTRAINT check_valid_json
        CHECK (
            (prompt_template IS NULL OR jsonb_typeof(prompt_template) = 'object') AND
            (model_params IS NULL OR jsonb_typeof(model_params) = 'object')
        )
);

-- Chain Evaluations table
-- Links chains to sessions and tracks evaluation runs
CREATE TABLE chain_evaluations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL,
    chain_id UUID NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    CONSTRAINT fk_chain_evaluations_session
        FOREIGN KEY (session_id)
        REFERENCES sessions(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_chain_evaluations_chain
        FOREIGN KEY (chain_id)
        REFERENCES chains(id)
        ON DELETE CASCADE,
    
    -- Indexes
    CREATE INDEX idx_chain_evaluations_session_id ON chain_evaluations(session_id),
    CREATE INDEX idx_chain_evaluations_chain_id ON chain_evaluations(chain_id)
);

-- Answers table
-- Stores generated answers and their evaluation metrics
CREATE TABLE answers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    evaluation_id UUID NOT NULL,
    question_id UUID NOT NULL,
    config_id UUID NOT NULL,
    generated_text TEXT NOT NULL,
    score score_range,
    generated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    CONSTRAINT fk_answers_evaluation
        FOREIGN KEY (evaluation_id)
        REFERENCES chain_evaluations(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_answers_question
        FOREIGN KEY (question_id)
        REFERENCES questions(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_answers_config
        FOREIGN KEY (config_id)
        REFERENCES configurations(id)
        ON DELETE CASCADE,
    
    -- Indexes
    CREATE INDEX idx_answers_evaluation_id ON answers(evaluation_id),
    CREATE INDEX idx_answers_question_id ON answers(question_id),
    CREATE INDEX idx_answers_config_id ON answers(config_id)
);

-- Answer Comments table
-- Stores multiple comments for each answer
CREATE TABLE answer_comments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    answer_id UUID NOT NULL,
    comment_text TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    CONSTRAINT fk_answer_comments_answer
        FOREIGN KEY (answer_id)
        REFERENCES answers(id)
        ON DELETE CASCADE,
    
    -- Indexes
    CREATE INDEX idx_answer_comments_answer_id ON answer_comments(answer_id)
);


-- Triggers for updated_at timestamps

-- Step 1: Create the trigger function to update last_accessed
CREATE OR REPLACE FUNCTION update_last_accessed()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_accessed := CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Step 2: Create the trigger to call the function on update
CREATE TRIGGER trigger_update_last_accessed
BEFORE UPDATE ON sessions
FOR EACH ROW
EXECUTE FUNCTION update_last_accessed();


-- Create views for common queries
CREATE VIEW latest_session_activity AS
SELECT 
    s.id,
    s.name,
    s.description,
    s.created_at,
    s.last_accessed,
    COUNT(DISTINCT ce.chain_id) as chain_count,
    COUNT(DISTINCT q.id) as question_count,
    COUNT(DISTINCT a.id) as answer_count
FROM sessions s
LEFT JOIN chain_evaluations ce ON s.id = ce.session_id
LEFT JOIN questions q ON s.id = q.session_id
LEFT JOIN answers a ON ce.id = a.evaluation_id
GROUP BY s.id, s.name, s.description, s.created_at, s.last_accessed
ORDER BY s.last_accessed DESC;

-- Create view for answers with their latest comments
CREATE VIEW answers_with_comments AS
SELECT 
    a.*,
    array_agg(ac.comment_text ORDER BY ac.created_at ASC) as comments
FROM answers a
LEFT JOIN answer_comments ac ON a.id = ac.answer_id
GROUP BY a.id;

-- Add comments to tables
COMMENT ON TABLE sessions IS 'Stores evaluation sessions for LangChain expression chains';
COMMENT ON TABLE chains IS 'Represents individual LangChain expression chains imported from files';
COMMENT ON TABLE questions IS 'Contains evaluation questions with optional expected answers';
COMMENT ON TABLE configurations IS 'Stores chain configurations including prompt templates and model parameters';
COMMENT ON TABLE chain_evaluations IS 'Tracks evaluation runs linking chains to sessions';
COMMENT ON TABLE answers IS 'Stores generated answers and their evaluation metrics';
COMMENT ON TABLE answer_comments IS 'Stores multiple comments for each answer';
COMMENT ON VIEW latest_session_activity IS 'Provides an overview of session activity with related counts';
COMMENT ON VIEW answers_with_comments IS 'Provides answers with their comments as an array';