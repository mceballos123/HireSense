-- Hiring Evaluations Table for Supabase
-- This table stores the results of the uAgents hiring system evaluations

CREATE TABLE IF NOT EXISTS hiring_evaluations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidate_name TEXT NOT NULL,
    job_title TEXT NOT NULL,
    resume_summary TEXT,
    job_summary TEXT,
    intersection_score FLOAT8,
    intersection_notes TEXT,
    pro_arguments JSONB,
    anti_arguments JSONB,
    final_decision TEXT CHECK (final_decision IN ('HIRE', 'REJECT')),
    decision_confidence FLOAT8,
    decision_reasoning TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create an index on candidate_name for faster lookups
CREATE INDEX IF NOT EXISTS idx_hiring_evaluations_candidate_name ON hiring_evaluations(candidate_name);

-- Create an index on job_title for faster lookups
CREATE INDEX IF NOT EXISTS idx_hiring_evaluations_job_title ON hiring_evaluations(job_title);

-- Create an index on final_decision for filtering
CREATE INDEX IF NOT EXISTS idx_hiring_evaluations_decision ON hiring_evaluations(final_decision);

-- Create an index on created_at for time-based queries
CREATE INDEX IF NOT EXISTS idx_hiring_evaluations_created_at ON hiring_evaluations(created_at);

-- Enable Row Level Security (RLS)
ALTER TABLE hiring_evaluations ENABLE ROW LEVEL SECURITY;

-- Create a policy that allows all operations (you can modify this based on your needs)
CREATE POLICY "Allow all operations on hiring_evaluations" ON hiring_evaluations
    FOR ALL USING (true);

-- Create a function to automatically update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create a trigger to automatically update the updated_at column
CREATE TRIGGER update_hiring_evaluations_updated_at 
    BEFORE UPDATE ON hiring_evaluations 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column(); 