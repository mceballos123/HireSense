# AI Hiring Agent System

A multi-agent hiring system using uAgents and ASI:One LLM for intelligent candidate evaluation and decision-making.

## Overview

This system implements a sophisticated hiring process using multiple AI agents that work together to:
1. Parse and analyze job descriptions
2. Parse and analyze candidate resumes
3. Evaluate the intersection between job requirements and candidate qualifications
4. Conduct a multi-round debate between pro-hire and anti-hire advocates
5. Make a final hiring decision based on all arguments

## Architecture

### Agents

1. **JobParserAgent** - Analyzes job descriptions using LLM to extract:
   - Required skills
   - Preferred skills
   - Experience level
   - Key requirements

2. **ResumeParserAgent** - Analyzes candidate resumes using LLM to extract:
   - Technical skills
   - Years of experience
   - Experience level
   - Key achievements

3. **IntersectionAgent** - Evaluates the match between job and candidate:
   - Matching skills
   - Missing skills
   - Experience compatibility
   - Overall compatibility score
   - Strengths and weaknesses

4. **ProHireAgent** - Advocates FOR hiring the candidate:
   - Builds compelling arguments for hiring
   - Focuses on strengths and potential
   - Responds to anti-hire arguments

5. **AntiHireAgent** - Advocates AGAINST hiring the candidate:
   - Builds compelling arguments against hiring
   - Focuses on gaps and risks
   - Responds to pro-hire arguments

6. **DecisionAgent** - Makes the final hiring decision:
   - Evaluates all debate arguments
   - Considers compatibility scores
   - Provides reasoning and confidence

### Communication Flow

```
Job Description → JobParserAgent
Resume → ResumeParserAgent
                    ↓
            IntersectionAgent
                    ↓
            Debate (3 rounds each)
    ProHireAgent ↔ AntiHireAgent
                    ↓
            DecisionAgent
                    ↓
            Final Decision
```

## Features

- **LLM-Powered Analysis**: Each agent uses ASI:One LLM for intelligent text analysis
- **Multi-Round Debate**: Pro and anti agents engage in 3 rounds of debate
- **Structured Output**: All agents return structured JSON responses
- **Confidence Scoring**: Each decision includes confidence levels
- **Graceful Fallbacks**: System works even with API connection issues
- **uAgents Integration**: Full uAgents implementation for distributed communication

## Files

- `hiring_agents.py` - Full uAgents implementation with distributed agents
- `simple_hiring_demo.py` - Simplified demo showing agent logic and prompts
- `requirements.txt` - Python dependencies

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Simple Demo (Recommended for testing)

```bash
python3 simple_hiring_demo.py
```

This runs a complete hiring evaluation with sample data and shows the full process.

### Full uAgents Implementation

```bash
python3 hiring_agents.py
```

This runs the complete distributed agent system using uAgents.

## Configuration

### ASI:One API Setup

1. Get your API key from [ASI:One](https://asi.one)
2. Update the `ASI_API_KEY` in the code files
3. The system will automatically use the LLM for intelligent analysis

### Custom Data

To use your own job descriptions and resumes, modify the test data in the main functions:

```python
resume_content = """
Your candidate's resume content here...
"""

job_description = """
Your job description here...
"""
```

## Output Format

The system provides detailed output including:

- **Job Analysis**: Extracted skills, requirements, and analysis
- **Resume Analysis**: Candidate skills, experience, and achievements
- **Intersection Analysis**: Compatibility score and match details
- **Debate Arguments**: 3 rounds of pro and anti arguments
- **Final Decision**: Hire/No Hire with confidence and reasoning

## Example Output

```
🤖 Starting Hiring Evaluation Process
============================================================

📋 STEP 1: Parsing Job and Resume
💼 job_parser: Parsing job description for Software Engineer
📄 resume_parser: Parsing resume for John Doe

🔍 STEP 2: Evaluating Intersection
🔍 intersection_evaluator: Evaluating intersection
Overall Compatibility: 0.85

⚖️ STEP 3: Conducting Debate
✅ pro_hire_advocate: Building pro-hire argument (round 1)
❌ anti_hire_advocate: Building anti-hire argument (round 1)
...

🎯 STEP 4: Making Final Decision

============================================================
FINAL HIRING DECISION
============================================================
Decision: HIRE
Confidence: 0.85
Reasoning: Strong skills match and good potential
Key Factors: Technical skills, Experience level, Growth potential
============================================================
```

## Extending the System

### Adding New Agents

1. Create a new agent class inheriting from `SimpleLLMAgent` or `LLMAgent`
2. Implement the required methods with appropriate prompts
3. Add the agent to the coordinator

### Customizing Prompts

Each agent has specific prompts that can be customized for different use cases:
- Job parsing prompts for different industries
- Resume parsing prompts for different roles
- Debate prompts for different evaluation criteria

### Integration with Other Systems

The system can be integrated with:
- HR management systems
- Applicant tracking systems
- Interview scheduling systems
- Performance evaluation systems

## Troubleshooting

### API Connection Issues

If you see "API Error" messages, the system will use default values and continue working. To fix:
1. Check your internet connection
2. Verify your ASI:One API key
3. Ensure the API endpoint is accessible

### uAgents Issues

If the full uAgents implementation doesn't work:
1. Use the simple demo version
2. Check uAgents installation
3. Verify port availability

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of the AI Berkeley Hackathon.
