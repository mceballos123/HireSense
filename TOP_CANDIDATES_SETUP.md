# Dynamic Top Candidates Feature

This document explains the new dynamic top candidates feature that automatically populates the main dashboard with candidates who score 85% or higher in the hiring evaluation system.

## Overview

The system now automatically:

1. **Saves high-scoring candidates**: When the decision agent evaluates a candidate with 85%+ confidence, they're automatically saved to the database
2. **Displays live data**: The frontend dashboard can now show real candidates from evaluations instead of hardcoded data
3. **Provides API access**: RESTful endpoints allow fetching top candidates data

## Database Schema

A new `top_candidates` table has been added with the following structure:

```sql
CREATE TABLE top_candidates (
    id uuid PRIMARY KEY,
    candidate_name text NOT NULL,
    job_title text NOT NULL,
    overall_score float8 NOT NULL CHECK (overall_score >= 85.0),
    confidence float8 NOT NULL,
    decision text CHECK (decision IN ('HIRE', 'REJECT')),
    -- ... additional candidate information
);
```

## Setup Instructions

### 1. Database Setup

Run the updated SQL schema in your Supabase database:

```bash
# The schema is in backend/db/supabase_setup.sql
# Copy the new top_candidates table section and run it in Supabase SQL editor
```

### 2. Backend Setup

The backend automatically saves high-scoring candidates. No additional configuration needed.

### 3. Frontend Setup

The dashboard now has a toggle button to switch between:

- **Live Data**: Real candidates from the evaluation system (85%+ confidence)
- **Demo Data**: The original hardcoded sample data

### 4. Testing

Test the functionality using the provided test script:

```bash
cd backend
python test_top_candidates.py
```

## API Endpoints

### Get Top Candidates

```
GET /top-candidates?limit=20&min_score=85.0
```

### Get Specific Candidate

```
GET /top-candidates/{candidate_id}
```

### Get Candidates for Job

```
GET /job-postings/{job_id}/top-candidates
```

## How It Works

### 1. Evaluation Process

When a resume is evaluated through the hiring agents system:

1. **Resume Parser Agent** → extracts candidate information
2. **Job Parser Agent** → extracts job requirements
3. **Intersection Agent** → calculates compatibility
4. **Pro/Anti Hire Agents** → debate the hire decision
5. **Decision Agent** → makes final decision with confidence score

### 2. Automatic Storage

If the decision confidence is ≥ 85%:

- **Decision Agent** automatically calls `_save_top_candidate()`
- Candidate data is stored in the `top_candidates` table
- Duplicates are prevented by checking existing records

### 3. Dashboard Display

The frontend dashboard:

- Fetches live data from `/top-candidates` API endpoint
- Transforms backend data to match frontend component structure
- Falls back to demo data if API is unavailable
- Provides toggle to switch between live and demo data

## Usage Example

1. **Submit a resume** through the resume evaluation feature
2. **Enter a candidate name** (e.g., "Jon Snow")
3. **Let the system evaluate** the resume against job requirements
4. **If confidence ≥ 85%**, candidate automatically appears on main dashboard
5. **View live candidates** by clicking "Live Data" toggle on dashboard

## Features

- ✅ **Automatic Population**: No manual data entry required
- ✅ **Real-time Updates**: New high-scoring candidates appear immediately
- ✅ **Quality Threshold**: Only candidates with 85%+ confidence are shown
- ✅ **Fallback Support**: Graceful degradation to demo data if needed
- ✅ **API Integration**: RESTful endpoints for external integration
- ✅ **Duplicate Prevention**: Same candidate won't be added multiple times for same job

## Data Flow

```
Resume Upload → Evaluation Pipeline → Decision Agent
                                          ↓ (if score ≥ 85%)
                                   top_candidates table
                                          ↓
                              API Endpoint (/top-candidates)
                                          ↓
                                 Frontend Dashboard
```

## Configuration

### Confidence Threshold

Change the minimum confidence threshold in:

- **Decision Agent**: `backend/hiring_agents/decision_agent.py` (line 107)
- **Database**: `backend/db/supabase_setup.sql` (CHECK constraint)
- **API**: `backend/api/job_postings.py` (default min_score parameter)

### Frontend API URL

Update the API URL in:

- **Dashboard Component**: `frontend/src/components/dashboard/dashboard-content.tsx` (line 130)

## Troubleshooting

### No Candidates Appearing

1. Verify database schema is applied
2. Check backend server is running on port 8000
3. Ensure evaluations are completing with ≥ 85% confidence
4. Check browser console for API errors

### API Connection Issues

1. Verify CORS settings in `backend/api/main.py`
2. Check Supabase credentials in `backend/db/supabase_client.py`
3. Ensure frontend is making requests to correct backend URL

### Performance

- Database indexes are created for common queries
- API responses are limited to prevent large payloads
- Frontend implements loading states and error handling

