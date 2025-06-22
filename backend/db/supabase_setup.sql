-- Hiring Evaluations Table for Supabase
-- This table stores the results of the uAgents hiring system evaluations

-- First, create the resumes table for storing parsed resume data
CREATE TABLE IF NOT EXISTS resumes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidate_name TEXT NOT NULL,
    original_filename TEXT,
    resume_text TEXT NOT NULL,
    text_length INTEGER,
    upload_timestamp TIMESTAMP DEFAULT NOW(),
    
    -- Parsed resume analysis
    skills JSONB,
    experience_years INTEGER,
    experience_level TEXT,
    key_achievements JSONB,
    analysis_summary TEXT,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for the resumes table
CREATE INDEX IF NOT EXISTS idx_resumes_candidate_name ON resumes(candidate_name);
CREATE INDEX IF NOT EXISTS idx_resumes_experience_level ON resumes(experience_level);
CREATE INDEX IF NOT EXISTS idx_resumes_created_at ON resumes(created_at);

-- Now create the hiring evaluations table with reference to resumes
CREATE TABLE IF NOT EXISTS hiring_evaluations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    resume_id UUID REFERENCES resumes(id) ON DELETE CASCADE,
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

-- Create an index on resume_id for linking
CREATE INDEX IF NOT EXISTS idx_hiring_evaluations_resume_id ON hiring_evaluations(resume_id);

-- Enable Row Level Security (RLS)
ALTER TABLE resumes ENABLE ROW LEVEL SECURITY;
ALTER TABLE hiring_evaluations ENABLE ROW LEVEL SECURITY;

-- Create policies that allow all operations (you can modify this based on your needs)
CREATE POLICY "Allow all operations on resumes" ON resumes
    FOR ALL USING (true);

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

-- Create triggers to automatically update the updated_at column
CREATE TRIGGER update_resumes_updated_at 
    BEFORE UPDATE ON resumes 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_hiring_evaluations_updated_at 
    BEFORE UPDATE ON hiring_evaluations 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column(); 

-- Job Postings Table for Supabase
-- This table stores job postings

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS public.job_postings (
    id uuid primary key default gen_random_uuid(),
    title text not null,
    description text,
    skills text[], -- or use jsonb if you want more structure
    location text,
    employment_type text,
    status text default 'ACTIVE' check (status in ('ACTIVE', 'INACTIVE')),
    applicants_count integer default 0,
    posted_at timestamp default now(),
    updated_at timestamp default now()
);

-- Indexes for faster lookups
CREATE INDEX IF NOT EXISTS idx_job_postings_title on job_postings(title);
CREATE INDEX IF NOT EXISTS idx_job_postings_status on job_postings(status);
CREATE INDEX IF NOT EXISTS idx_job_postings_posted_at on job_postings(posted_at);

-- Enable Row Level Security (RLS)
ALTER TABLE job_postings ENABLE ROW LEVEL SECURITY;

-- Allow all operations (for dev, restrict as needed)
CREATE POLICY "Allow all operations on job_postings" ON job_postings
    FOR ALL USING (true);

-- Auto-update updated_at on row update
CREATE OR REPLACE FUNCTION update_job_postings_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_job_postings_updated_at
    BEFORE UPDATE ON job_postings
    FOR EACH ROW
    EXECUTE FUNCTION update_job_postings_updated_at(); 