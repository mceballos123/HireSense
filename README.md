# HireSense

## Software Architecture

<img width="478" alt="Screenshot 2025-06-24 at 11 14 06 AM" src="https://github.com/user-attachments/assets/e37e090b-65c0-4c47-a5fe-87667ed71ac1" />

<img width="838" alt="Screenshot 2025-06-24 at 11 14 48 AM" src="https://github.com/user-attachments/assets/fb592c60-48fd-49de-9fcc-fcc5c1c47164" />

## Introduction
Traditional Applicant Tracking Systems (ATS) are broken. They rely heavily on exact keyword matching to rank resumes, which creates two major problems:

  1. Qualified candidates often get rejected because they phrase their experiences differently.

  2. Unqualified candidates beat the system by keyword stuffing their resumes with buzzwords.

Even with automation, recruiters remain overwhelmed, spending hours manually reviewing large stacks of resumes, often without intelligent assistance. We asked ourselves: what if an AI could simulate a real hiring panel — one that is explainable, fair, and nuanced?

That’s why we built HireSense AI HR Council — a smarter, agentic alternative to traditional ATS.

## What It Does
HireSense is an autonomous hiring pipeline composed of multiple specialized AI agents that work together like a hiring committee:
  
  1. ResumeAgent extracts hard facts from candidates’ resumes, such as skills, years of experience, certifications, and project names.
  
  2. JobAgent breaks down the job description into structured requirements: required skills, level, location, and nice-to-haves.
  
  3. EvalAgent compares ResumeAgent and JobAgent data, highlights alignment or gaps, and produces a match score.
  
  4. DebateAgent1 — The Optimist tailors the candidate’s strengths to fit the job.
  
  5. DebateAgent2 — The Skeptic points out inconsistencies, missing skills, or red flags.
  
  6. DebateAgent3 — The Arbiter observes the debate and makes an informed judgment.
  
  7. FinalAgent synthesizes all information and makes a hiring recommendation.

Together, these agents simulate a real hiring debate with structured reasoning, providing an explainable and fair evaluation rather than relying on keyword matching alone.


## How We Built It
We leveraged cutting-edge technologies to build HireSense:

  -Fetch.ai uAgents to modularize each AI agent (ResumeAgent, JobAgent, etc.)
  
  -ASI One to power intelligence and reasoning behind agent responses
  
  -Model Context Protocol (MCP) framework to manage communication and memory between agents
  
  -Supabase to log results and store top candidates
  
  -Python and FastAPI for backend logic
  
  -Deployed locally and tested endpoints using Postman

This was our first time working with uAgents, ASI One, and MCP — learning how to manage agent messaging, memory, and context sharing was both challenging and rewarding.

## Tech Stack

- **Agent Framework**: Fetch.ai uAgents
- **AI Integration**: ASI One, Fetch.ai
- **Backend**: Python, FastAPI, Supabase
- **Frontend**: Next.js, Tailwind CSS

### Installation
```
1. Clone the repository
2. 
git clone <repository-url>
cd HireSense
```



2. Install dependencies
```
npm install
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with required environment variables:
```
Example .env file
NEXT_PUBLIC_API_URL=http://localhost:8000
ASI_API_KEY=your_asi_api_key
ASI_API_URL=your_asi_api_url
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

4. Start the development servers
```
python backend/main.py
uvicorn api/main:app --reload
npm run dev
```




