"""
Hiring Agent System
==================

A multi-agent hiring system using uAgents and ASI:One LLM.
Each agent has its own prompt and communicates with others to make hiring decisions.

Agents:
1. JobParserAgent - Parses job descriptions
2. ResumeParserAgent - Parses resumes
3. IntersectionAgent - Finds intersection between job and resume
4. ProHireAgent - Advocates for hiring
5. AntiHireAgent - Advocates against hiring
6. DecisionAgent - Makes final hiring decision
"""

import asyncio
import json
import aiohttp
from uagents import Agent, Context, Protocol
from uagents.setup import fund_agent_if_low
from pydantic import BaseModel
from typing import List, Dict, Optional

# ASI:One API configuration
ASI_API_KEY = "sk_d1a256183aa249f49f49d649dddff42ca039df035fb7404394efe289149d9997"
ASI_API_URL = "https://api.asi1.ai/v1/chat/completions"

# Message models
class JobParseRequest(BaseModel):
    job_description: str
    job_title: str

class JobParseResponse(BaseModel):
    job_title: str
    required_skills: List[str]
    preferred_skills: List[str]
    experience_level: str
    key_requirements: List[str]
    analysis: str

class ResumeParseRequest(BaseModel):
    resume_content: str
    candidate_name: str

class ResumeParseResponse(BaseModel):
    candidate_name: str
    skills: List[str]
    experience_years: int
    experience_level: str
    key_achievements: List[str]
    analysis: str

class IntersectionRequest(BaseModel):
    job_analysis: JobParseResponse
    resume_analysis: ResumeParseResponse

class IntersectionResponse(BaseModel):
    matching_skills: List[str]
    missing_skills: List[str]
    experience_match: bool
    overall_compatibility: float
    strengths: List[str]
    weaknesses: List[str]
    analysis: str

class DebateRequest(BaseModel):
    intersection_analysis: IntersectionResponse
    round_number: int
    previous_argument: str = ""

class DebateResponse(BaseModel):
    position: str  # "pro" or "anti"
    argument: str
    confidence: float
    key_points: List[str]

class DecisionRequest(BaseModel):
    pro_arguments: List[DebateResponse]
    anti_arguments: List[DebateResponse]
    intersection_analysis: IntersectionResponse

class DecisionResponse(BaseModel):
    decision: str  # "hire" or "no_hire"
    confidence: float
    reasoning: str
    key_factors: List[str]

# Base LLM Agent class
class LLMAgent(Agent):
    def __init__(self, name: str, port: int, seed: str):
        super().__init__(name=name, port=port, seed=seed)
        fund_agent_if_low(self.wallet.address())
        self.api_key = ASI_API_KEY
        self.api_url = ASI_API_URL
    
    async def query_llm(self, prompt: str) -> dict:
        """Query ASI1.ai API with a prompt and get response"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        payload = {
            "model": "asi1-mini",
            "messages": [
                {"role": "system", "content": "You are a specialized AI agent for hiring analysis. Provide clear, structured responses."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "stream": False,
            "max_tokens": 800
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.api_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        return {
                            "success": True,
                            "content": result["choices"][0]["message"]["content"]
                        }
                    else:
                        return {
                            "success": False,
                            "content": f"API Error: {response.status}"
                        }
        except Exception as e:
            return {
                "success": False,
                "content": f"Request Error: {str(e)}"
            }

# Job Parser Agent
class JobParserAgent(LLMAgent):
    def __init__(self):
        super().__init__("job_parser", 8001, "job_parser_seed")
        
        self.protocol = Protocol()
        
        @self.protocol.on_message(model=JobParseRequest)
        async def handle_job_parse(ctx: Context, sender: str, msg: JobParseRequest):
            print(f"💼 {self.name}: Parsing job description for {msg.job_title}")
            
            prompt = f"""
            Analyze the following job description and extract key information.
            
            Job Title: {msg.job_title}
            Job Description:
            {msg.job_description}
            
            Extract and analyze:
            1. Required skills (must-have technical skills)
            2. Preferred skills (nice-to-have skills)
            3. Experience level (Junior, Mid-level, Senior)
            4. Key requirements and responsibilities
            
            Respond with ONLY a JSON object in this exact format:
            {{
                "required_skills": ["skill1", "skill2"],
                "preferred_skills": ["skill3", "skill4"],
                "experience_level": "<Junior/Mid-level/Senior>",
                "key_requirements": ["req1", "req2"],
                "analysis": "<brief analysis of the job requirements>"
            }}
            """
            
            result = await self.query_llm(prompt)
            
            if result["success"]:
                try:
                    analysis = json.loads(result["content"])
                    response = JobParseResponse(
                        job_title=msg.job_title,
                        required_skills=analysis["required_skills"],
                        preferred_skills=analysis["preferred_skills"],
                        experience_level=analysis["experience_level"],
                        key_requirements=analysis["key_requirements"],
                        analysis=analysis["analysis"]
                    )
                except (json.JSONDecodeError, KeyError):
                    response = JobParseResponse(
                        job_title=msg.job_title,
                        required_skills=["python", "javascript"],
                        preferred_skills=["react"],
                        experience_level="Mid-level",
                        key_requirements=["web development"],
                        analysis="Failed to parse LLM response, using defaults"
                    )
            else:
                response = JobParseResponse(
                    job_title=msg.job_title,
                    required_skills=["python", "javascript"],
                    preferred_skills=["react"],
                    experience_level="Mid-level",
                    key_requirements=["web development"],
                    analysis=f"API Error: {result['content']}"
                )
            
            print(f"💼 {self.name}: Job parsing complete")
            await ctx.send(sender, response)
        
        self.include(self.protocol)

# Resume Parser Agent
class ResumeParserAgent(LLMAgent):
    def __init__(self):
        super().__init__("resume_parser", 8002, "resume_parser_seed")
        
        self.protocol = Protocol()
        
        @self.protocol.on_message(model=ResumeParseRequest)
        async def handle_resume_parse(ctx: Context, sender: str, msg: ResumeParseRequest):
            print(f"📄 {self.name}: Parsing resume for {msg.candidate_name}")
            
            prompt = f"""
            Analyze the following resume and extract key information.
            
            Candidate Name: {msg.candidate_name}
            Resume Content:
            {msg.resume_content}
            
            Extract and analyze:
            1. Technical skills (programming languages, frameworks, tools)
            2. Years of experience
            3. Experience level (Junior, Mid-level, Senior)
            4. Key achievements and accomplishments
            
            Respond with ONLY a JSON object in this exact format:
            {{
                "skills": ["skill1", "skill2", "skill3"],
                "experience_years": <number>,
                "experience_level": "<Junior/Mid-level/Senior>",
                "key_achievements": ["achievement1", "achievement2"],
                "analysis": "<brief analysis of the candidate's profile>"
            }}
            """
            
            result = await self.query_llm(prompt)
            
            if result["success"]:
                try:
                    analysis = json.loads(result["content"])
                    response = ResumeParseResponse(
                        candidate_name=msg.candidate_name,
                        skills=analysis["skills"],
                        experience_years=analysis["experience_years"],
                        experience_level=analysis["experience_level"],
                        key_achievements=analysis["key_achievements"],
                        analysis=analysis["analysis"]
                    )
                except (json.JSONDecodeError, KeyError):
                    response = ResumeParseResponse(
                        candidate_name=msg.candidate_name,
                        skills=["python", "javascript"],
                        experience_years=2,
                        experience_level="Mid-level",
                        key_achievements=["web development"],
                        analysis="Failed to parse LLM response, using defaults"
                    )
            else:
                response = ResumeParseResponse(
                    candidate_name=msg.candidate_name,
                    skills=["python", "javascript"],
                    experience_years=2,
                    experience_level="Mid-level",
                    key_achievements=["web development"],
                    analysis=f"API Error: {result['content']}"
                )
            
            print(f"📄 {self.name}: Resume parsing complete")
            await ctx.send(sender, response)
        
        self.include(self.protocol)

# Intersection Agent
class IntersectionAgent(LLMAgent):
    def __init__(self):
        super().__init__("intersection_evaluator", 8003, "intersection_seed")
        
        self.protocol = Protocol()
        
        @self.protocol.on_message(model=IntersectionRequest)
        async def handle_intersection(ctx: Context, sender: str, msg: IntersectionRequest):
            print(f"🔍 {self.name}: Evaluating intersection")
            
            prompt = f"""
            Analyze the intersection between the job requirements and candidate profile.
            
            Job Analysis:
            {msg.job_analysis.analysis}
            Required Skills: {msg.job_analysis.required_skills}
            Preferred Skills: {msg.job_analysis.preferred_skills}
            Experience Level: {msg.job_analysis.experience_level}
            
            Candidate Analysis:
            {msg.resume_analysis.analysis}
            Skills: {msg.resume_analysis.skills}
            Experience: {msg.resume_analysis.experience_years} years ({msg.resume_analysis.experience_level})
            Achievements: {msg.resume_analysis.key_achievements}
            
            Evaluate the match and provide:
            1. Matching skills between candidate and job
            2. Missing skills that the job requires
            3. Whether experience levels match
            4. Overall compatibility score (0.0 to 1.0)
            5. Key strengths and weaknesses
            
            Respond with ONLY a JSON object in this exact format:
            {{
                "matching_skills": ["skill1", "skill2"],
                "missing_skills": ["skill3", "skill4"],
                "experience_match": <true/false>,
                "overall_compatibility": <0.0 to 1.0>,
                "strengths": ["strength1", "strength2"],
                "weaknesses": ["weakness1", "weakness2"],
                "analysis": "<comprehensive analysis of the match>"
            }}
            """
            
            result = await self.query_llm(prompt)
            
            if result["success"]:
                try:
                    analysis = json.loads(result["content"])
                    response = IntersectionResponse(
                        matching_skills=analysis["matching_skills"],
                        missing_skills=analysis["missing_skills"],
                        experience_match=analysis["experience_match"],
                        overall_compatibility=analysis["overall_compatibility"],
                        strengths=analysis["strengths"],
                        weaknesses=analysis["weaknesses"],
                        analysis=analysis["analysis"]
                    )
                except (json.JSONDecodeError, KeyError):
                    response = IntersectionResponse(
                        matching_skills=["python", "javascript"],
                        missing_skills=[],
                        experience_match=True,
                        overall_compatibility=0.7,
                        strengths=["Good technical skills"],
                        weaknesses=[],
                        analysis="Failed to parse LLM response, using defaults"
                    )
            else:
                response = IntersectionResponse(
                    matching_skills=["python", "javascript"],
                    missing_skills=[],
                    experience_match=True,
                    overall_compatibility=0.7,
                    strengths=["Good technical skills"],
                    weaknesses=[],
                    analysis=f"API Error: {result['content']}"
                )
            
            print(f"🔍 {self.name}: Intersection evaluation complete")
            await ctx.send(sender, response)
        
        self.include(self.protocol)

# Pro-Hire Debate Agent
class ProHireAgent(LLMAgent):
    def __init__(self):
        super().__init__("pro_hire_advocate", 8004, "pro_hire_seed")
        
        self.protocol = Protocol()
        
        @self.protocol.on_message(model=DebateRequest)
        async def handle_debate(ctx: Context, sender: str, msg: DebateRequest):
            print(f"✅ {self.name}: Building pro-hire argument (round {msg.round_number})")
            
            context = f"Previous argument: {msg.previous_argument}" if msg.previous_argument else "First round of debate"
            
            prompt = f"""
            You are advocating FOR hiring this candidate. Build a compelling argument based on the intersection analysis.
            
            Intersection Analysis:
            {msg.intersection_analysis.analysis}
            Matching Skills: {msg.intersection_analysis.matching_skills}
            Strengths: {msg.intersection_analysis.strengths}
            Overall Compatibility: {msg.intersection_analysis.overall_compatibility}
            
            Context: {context}
            Round: {msg.round_number}
            
            Build a strong argument FOR hiring this candidate. Focus on:
            1. How the candidate's strengths align with the job
            2. Why the matching skills are valuable
            3. Potential for growth and learning
            4. Why the candidate would be a good fit
            
            Respond with ONLY a JSON object in this exact format:
            {{
                "argument": "<your compelling argument for hiring>",
                "confidence": <0.0 to 1.0>,
                "key_points": ["point1", "point2", "point3"]
            }}
            """
            
            result = await self.query_llm(prompt)
            
            if result["success"]:
                try:
                    analysis = json.loads(result["content"])
                    response = DebateResponse(
                        position="pro",
                        argument=analysis["argument"],
                        confidence=analysis["confidence"],
                        key_points=analysis["key_points"]
                    )
                except (json.JSONDecodeError, KeyError):
                    response = DebateResponse(
                        position="pro",
                        argument="Candidate shows good potential and matching skills",
                        confidence=0.7,
                        key_points=["Good skills match", "Potential for growth"]
                    )
            else:
                response = DebateResponse(
                    position="pro",
                    argument="Candidate shows good potential and matching skills",
                    confidence=0.7,
                    key_points=["Good skills match", "Potential for growth"]
                )
            
            print(f"✅ {self.name}: Pro-hire argument complete")
            await ctx.send(sender, response)
        
        self.include(self.protocol)

# Anti-Hire Debate Agent
class AntiHireAgent(LLMAgent):
    def __init__(self):
        super().__init__("anti_hire_advocate", 8005, "anti_hire_seed")
        
        self.protocol = Protocol()
        
        @self.protocol.on_message(model=DebateRequest)
        async def handle_debate(ctx: Context, sender: str, msg: DebateRequest):
            print(f"❌ {self.name}: Building anti-hire argument (round {msg.round_number})")
            
            context = f"Previous argument: {msg.previous_argument}" if msg.previous_argument else "First round of debate"
            
            prompt = f"""
            You are advocating AGAINST hiring this candidate. Build a compelling argument based on the intersection analysis.
            
            Intersection Analysis:
            {msg.intersection_analysis.analysis}
            Missing Skills: {msg.intersection_analysis.missing_skills}
            Weaknesses: {msg.intersection_analysis.weaknesses}
            Overall Compatibility: {msg.intersection_analysis.overall_compatibility}
            
            Context: {context}
            Round: {msg.round_number}
            
            Build a strong argument AGAINST hiring this candidate. Focus on:
            1. Critical skill gaps and missing requirements
            2. Why the weaknesses are concerning
            3. Risks of hiring someone with these gaps
            4. Why other candidates might be better
            
            Respond with ONLY a JSON object in this exact format:
            {{
                "argument": "<your compelling argument against hiring>",
                "confidence": <0.0 to 1.0>,
                "key_points": ["point1", "point2", "point3"]
            }}
            """
            
            result = await self.query_llm(prompt)
            
            if result["success"]:
                try:
                    analysis = json.loads(result["content"])
                    response = DebateResponse(
                        position="anti",
                        argument=analysis["argument"],
                        confidence=analysis["confidence"],
                        key_points=analysis["key_points"]
                    )
                except (json.JSONDecodeError, KeyError):
                    response = DebateResponse(
                        position="anti",
                        argument="Candidate has significant skill gaps",
                        confidence=0.6,
                        key_points=["Missing skills", "Experience concerns"]
                    )
            else:
                response = DebateResponse(
                    position="anti",
                    argument="Candidate has significant skill gaps",
                    confidence=0.6,
                    key_points=["Missing skills", "Experience concerns"]
                )
            
            print(f"❌ {self.name}: Anti-hire argument complete")
            await ctx.send(sender, response)
        
        self.include(self.protocol)

# Decision Agent
class DecisionAgent(LLMAgent):
    def __init__(self):
        super().__init__("decision_maker", 8006, "decision_seed")
        
        self.protocol = Protocol()
        
        @self.protocol.on_message(model=DecisionRequest)
        async def handle_decision(ctx: Context, sender: str, msg: DecisionRequest):
            print(f"🎯 {self.name}: Making final hiring decision")
            
            # Format debate arguments for the prompt
            pro_args = "\n".join([f"Round {i+1}: {arg.argument}" for i, arg in enumerate(msg.pro_arguments)])
            anti_args = "\n".join([f"Round {i+1}: {arg.argument}" for i, arg in enumerate(msg.anti_arguments)])
            
            prompt = f"""
            You are the final decision maker for a hiring decision. Evaluate all the arguments and make a final decision.
            
            Intersection Analysis:
            {msg.intersection_analysis.analysis}
            Overall Compatibility: {msg.intersection_analysis.overall_compatibility}
            
            Pro-Hire Arguments:
            {pro_args}
            
            Anti-Hire Arguments:
            {anti_args}
            
            Evaluate the strength of each side's arguments and make a final decision.
            Consider:
            1. Which side made stronger arguments
            2. The overall compatibility score
            3. The confidence levels of each argument
            4. The key factors that matter most for this role
            
            Respond with ONLY a JSON object in this exact format:
            {{
                "decision": "<hire/no_hire>",
                "confidence": <0.0 to 1.0>,
                "reasoning": "<detailed explanation of your decision>",
                "key_factors": ["factor1", "factor2", "factor3"]
            }}
            """
            
            result = await self.query_llm(prompt)
            
            if result["success"]:
                try:
                    analysis = json.loads(result["content"])
                    response = DecisionResponse(
                        decision=analysis["decision"],
                        confidence=analysis["confidence"],
                        reasoning=analysis["reasoning"],
                        key_factors=analysis["key_factors"]
                    )
                except (json.JSONDecodeError, KeyError):
                    response = DecisionResponse(
                        decision="hire",
                        confidence=0.7,
                        reasoning="Default decision based on compatibility",
                        key_factors=["Skills match", "Experience level"]
                    )
            else:
                response = DecisionResponse(
                    decision="hire",
                    confidence=0.7,
                    reasoning="Default decision based on compatibility",
                    key_factors=["Skills match", "Experience level"]
                )
            
            print(f"🎯 {self.name}: Decision made")
            await ctx.send(sender, response)
        
        self.include(self.protocol)

# Main Coordinator
class HiringCoordinator(Agent):
    def __init__(self):
        super().__init__("hiring_coordinator", 8007, "coordinator_seed")
        fund_agent_if_low(self.wallet.address())
        
        # Store agent addresses
        self.job_parser_address = None
        self.resume_parser_address = None
        self.intersection_address = None
        self.pro_hire_address = None
        self.anti_hire_address = None
        self.decision_address = None
        
        # Store results
        self.job_analysis = None
        self.resume_analysis = None
        self.intersection_analysis = None
        self.pro_arguments = []
        self.anti_arguments = []
        
        self.protocol = Protocol()
        
        # Handle responses from each agent
        @self.protocol.on_message(model=JobParseResponse)
        async def handle_job_response(ctx: Context, sender: str, msg: JobParseResponse):
            print(f"🤖 {self.name}: Received job analysis for {msg.job_title}")
            self.job_analysis = msg
            await self._check_and_proceed(ctx)
        
        @self.protocol.on_message(model=ResumeParseResponse)
        async def handle_resume_response(ctx: Context, sender: str, msg: ResumeParseResponse):
            print(f"🤖 {self.name}: Received resume analysis for {msg.candidate_name}")
            self.resume_analysis = msg
            await self._check_and_proceed(ctx)
        
        @self.protocol.on_message(model=IntersectionResponse)
        async def handle_intersection_response(ctx: Context, sender: str, msg: IntersectionResponse):
            print(f"🤖 {self.name}: Received intersection analysis")
            self.intersection_analysis = msg
            await self._start_debate(ctx)
        
        @self.protocol.on_message(model=DebateResponse)
        async def handle_debate_response(ctx: Context, sender: str, msg: DebateResponse):
            print(f"🤖 {self.name}: Received {msg.position} argument (confidence: {msg.confidence:.2f})")
            
            if msg.position == "pro":
                self.pro_arguments.append(msg)
            else:
                self.anti_arguments.append(msg)
            
            await self._continue_debate(ctx)
        
        @self.protocol.on_message(model=DecisionResponse)
        async def handle_decision_response(ctx: Context, sender: str, msg: DecisionResponse):
            print(f"\n" + "="*60)
            print("FINAL HIRING DECISION")
            print("="*60)
            print(f"Decision: {msg.decision.upper()}")
            print(f"Confidence: {msg.confidence:.2f}")
            print(f"Reasoning: {msg.reasoning}")
            print(f"Key Factors: {', '.join(msg.key_factors)}")
            print("="*60)
        
        self.include(self.protocol)
    
    async def _check_and_proceed(self, ctx: Context):
        """Check if we have both job and resume analysis, then proceed to intersection"""
        if self.job_analysis and self.resume_analysis:
            print(f"🤖 {self.name}: Both analyses complete, evaluating intersection")
            
            request = IntersectionRequest(
                job_analysis=self.job_analysis,
                resume_analysis=self.resume_analysis
            )
            await ctx.send(self.intersection_address, request)
    
    async def _start_debate(self, ctx: Context):
        """Start the debate between pro and anti hire agents"""
        print(f"🤖 {self.name}: Starting debate (round 1)")
        
        # Start with pro-hire argument
        pro_request = DebateRequest(
            intersection_analysis=self.intersection_analysis,
            round_number=1
        )
        await ctx.send(self.pro_hire_address, pro_request)
    
    async def _continue_debate(self, ctx: Context):
        """Continue the debate or end it and make decision"""
        total_rounds = len(self.pro_arguments) + len(self.anti_arguments)
        
        if total_rounds < 6:  # 3 rounds each = 6 total
            # Continue debate
            if len(self.pro_arguments) > len(self.anti_arguments):
                # Anti-hire's turn
                round_num = len(self.anti_arguments) + 1
                previous_arg = self.pro_arguments[-1].argument
                
                anti_request = DebateRequest(
                    intersection_analysis=self.intersection_analysis,
                    round_number=round_num,
                    previous_argument=previous_arg
                )
                await ctx.send(self.anti_hire_address, anti_request)
            else:
                # Pro-hire's turn
                round_num = len(self.pro_arguments) + 1
                previous_arg = self.anti_arguments[-1].argument if self.anti_arguments else ""
                
                pro_request = DebateRequest(
                    intersection_analysis=self.intersection_analysis,
                    round_number=round_num,
                    previous_argument=previous_arg
                )
                await ctx.send(self.pro_hire_address, pro_request)
        else:
            # Debate complete, make decision
            print(f"🤖 {self.name}: Debate complete, making final decision")
            
            decision_request = DecisionRequest(
                pro_arguments=self.pro_arguments,
                anti_arguments=self.anti_arguments,
                intersection_analysis=self.intersection_analysis
            )
            await ctx.send(self.decision_address, decision_request)

# Main execution function
async def run_hiring_system(resume_content: str, job_description: str, 
                          candidate_name: str, job_title: str):
    """Run the complete hiring system"""
    print("🚀 Starting Hiring Agent System")
    print("="*60)
    
    # Create all agents
    job_parser = JobParserAgent()
    resume_parser = ResumeParserAgent()
    intersection_evaluator = IntersectionAgent()
    pro_hire = ProHireAgent()
    anti_hire = AntiHireAgent()
    decision_maker = DecisionAgent()
    coordinator = HiringCoordinator()
    
    # Start all agents
    await job_parser.run()
    await resume_parser.run()
    await intersection_evaluator.run()
    await pro_hire.run()
    await anti_hire.run()
    await decision_maker.run()
    await coordinator.run()
    
    # Wait for initialization
    await asyncio.sleep(2)
    
    # Store addresses
    coordinator.job_parser_address = job_parser.address
    coordinator.resume_parser_address = resume_parser.address
    coordinator.intersection_address = intersection_evaluator.address
    coordinator.pro_hire_address = pro_hire.address
    coordinator.anti_hire_address = anti_hire.address
    coordinator.decision_address = decision_maker.address
    
    # Send initial requests
    print("📤 Sending job and resume for analysis...")
    
    job_request = JobParseRequest(
        job_description=job_description,
        job_title=job_title
    )
    await coordinator.send(coordinator.job_parser_address, job_request)
    
    resume_request = ResumeParseRequest(
        resume_content=resume_content,
        candidate_name=candidate_name
    )
    await coordinator.send(coordinator.resume_parser_address, resume_request)
    
    # Wait for completion
    await asyncio.sleep(30)
    
    # Stop all agents
    await job_parser.stop()
    await resume_parser.stop()
    await intersection_evaluator.stop()
    await pro_hire.stop()
    await anti_hire.stop()
    await decision_maker.stop()
    await coordinator.stop()
    
    print("✅ Hiring system completed!")

# Example usage
if __name__ == "__main__":
    # Test data
    resume_content = """
    Software Engineer with 3 years of experience in web development.
    Proficient in Python, JavaScript, React, and Node.js.
    Experience with MongoDB and AWS services.
    Led development of multiple production applications.
    Strong problem-solving skills and experience with agile methodologies.
    """
    
    job_description = """
    Mid-level Software Engineer position.
    Required skills: Python, JavaScript, React.
    Preferred skills: Node.js, MongoDB, AWS.
    Experience with microservices and cloud deployment preferred.
    Looking for someone with 2-5 years of experience.
    """
    
    # Run the system
    asyncio.run(run_hiring_system(
        resume_content=resume_content,
        job_description=job_description,
        candidate_name="John Doe",
        job_title="Software Engineer"
    )) 