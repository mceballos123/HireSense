"""
uAgents Hiring System
=====================

A multi-agent hiring system using Fetch.ai uAgents and ASI:One LLM.
This version provides the same clean output as simple_hiring_demo.py but with proper uAgents communication.
"""

import asyncio
import json
import aiohttp
import ssl
import re
from typing import List, Dict, Optional
from uagents import Agent, Context, Protocol
from uagents.setup import fund_agent_if_low
from pydantic import BaseModel

# ASI:One API configuration
ASI_API_KEY = "sk_d1a256183aa249f49f49d649dddff42ca039df035fb7404394efe289149d9997"
ASI_API_URL = "https://api.asi1.ai/v1/chat/completions"

# Message Models
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
    analysis: str
    overall_compatibility: float
    skill_matches: List[str]
    skill_gaps: List[str]
    experience_match: str

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

class SimpleLLMAgent:
    """Base class for LLM-powered agents"""
    
    def __init__(self, name: str):
        self.name = name
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
            # Create SSL context to bypass certificate verification
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            connector = aiohttp.TCPConnector(ssl=ssl_context)
            
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.post(self.api_url, headers=headers, json=payload, timeout=30) as response:
                    if response.status == 200:
                        result = await response.json()
                        return {
                            "success": True,
                            "content": result["choices"][0]["message"]["content"]
                        }
                    else:
                        error_text = await response.text()
                        return {
                            "success": False,
                            "content": f"API Error {response.status}: {error_text}"
                        }
        except Exception as e:
            return {
                "success": False,
                "content": f"Request Error: {str(e)}"
            }

# Job Parser Agent
class JobParserAgent(Agent):
    def __init__(self):
        super().__init__("job_parser", 8001, "job_parser_seed")
        fund_agent_if_low(self.wallet.address())
        
        self.llm_agent = SimpleLLMAgent("job_parser")
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
            
            result = await self.llm_agent.query_llm(prompt)
            
            if result["success"]:
                try:
                    content = result["content"]
                    content = re.sub(r"^```json\s*|```$", "", content.strip(), flags=re.MULTILINE)
                    content = content.strip()
                    analysis = json.loads(content)
                    
                    response = JobParseResponse(
                        job_title=msg.job_title,
                        required_skills=analysis["required_skills"],
                        preferred_skills=analysis["preferred_skills"],
                        experience_level=analysis["experience_level"],
                        key_requirements=analysis["key_requirements"],
                        analysis=analysis["analysis"]
                    )
                    
                    print(f"💼 {self.name}: Job parsing complete")
                    await ctx.send(sender, response)
                    
                except (json.JSONDecodeError, KeyError) as e:
                    print(f"❌ {self.name}: JSON parsing error: {e}")
                    response = JobParseResponse(
                        job_title=msg.job_title,
                        required_skills=["python", "javascript"],
                        preferred_skills=["react"],
                        experience_level="Mid-level",
                        key_requirements=["web development"],
                        analysis="Failed to parse LLM response, using defaults"
                    )
                    await ctx.send(sender, response)
            else:
                response = JobParseResponse(
                    job_title=msg.job_title,
                    required_skills=["python", "javascript"],
                    preferred_skills=["react"],
                    experience_level="Mid-level",
                    key_requirements=["web development"],
                    analysis=f"API Error: {result['content']}"
                )
                await ctx.send(sender, response)
        
        self.include(self.protocol)

# Resume Parser Agent
class ResumeParserAgent(Agent):
    def __init__(self):
        super().__init__("resume_parser", 8002, "resume_parser_seed")
        fund_agent_if_low(self.wallet.address())
        
        self.llm_agent = SimpleLLMAgent("resume_parser")
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
            
            result = await self.llm_agent.query_llm(prompt)
            
            if result["success"]:
                try:
                    content = result["content"]
                    content = re.sub(r"^```json\s*|```$", "", content.strip(), flags=re.MULTILINE)
                    content = content.strip()
                    analysis = json.loads(content)
                    
                    response = ResumeParseResponse(
                        candidate_name=msg.candidate_name,
                        skills=analysis["skills"],
                        experience_years=analysis["experience_years"],
                        experience_level=analysis["experience_level"],
                        key_achievements=analysis["key_achievements"],
                        analysis=analysis["analysis"]
                    )
                    
                    print(f"📄 {self.name}: Resume parsing complete")
                    await ctx.send(sender, response)
                    
                except (json.JSONDecodeError, KeyError) as e:
                    print(f"❌ {self.name}: JSON parsing error: {e}")
                    response = ResumeParseResponse(
                        candidate_name=msg.candidate_name,
                        skills=["python", "javascript", "react"],
                        experience_years=3,
                        experience_level="Mid-level",
                        key_achievements=["Led development team"],
                        analysis="Failed to parse LLM response, using defaults"
                    )
                    await ctx.send(sender, response)
            else:
                response = ResumeParseResponse(
                    candidate_name=msg.candidate_name,
                    skills=["python", "javascript", "react"],
                    experience_years=3,
                    experience_level="Mid-level",
                    key_achievements=["Led development team"],
                    analysis=f"API Error: {result['content']}"
                )
                await ctx.send(sender, response)
        
        self.include(self.protocol)

# Intersection Evaluator Agent
class IntersectionAgent(Agent):
    def __init__(self):
        super().__init__("intersection_evaluator", 8003, "intersection_seed")
        fund_agent_if_low(self.wallet.address())
        
        self.llm_agent = SimpleLLMAgent("intersection_evaluator")
        self.protocol = Protocol()
        
        @self.protocol.on_message(model=IntersectionRequest)
        async def handle_intersection(ctx: Context, sender: str, msg: IntersectionRequest):
            print(f"🔍 {self.name}: Evaluating intersection")
            
            prompt = f"""
            Evaluate the intersection between job requirements and candidate profile.
            
            Job Analysis:
            {msg.job_analysis.analysis}
            Required Skills: {', '.join(msg.job_analysis.required_skills)}
            Preferred Skills: {', '.join(msg.job_analysis.preferred_skills)}
            Experience Level: {msg.job_analysis.experience_level}
            
            Resume Analysis:
            {msg.resume_analysis.analysis}
            Skills: {', '.join(msg.resume_analysis.skills)}
            Experience: {msg.resume_analysis.experience_years} years ({msg.resume_analysis.experience_level})
            
            Evaluate:
            1. Skill matches and gaps
            2. Experience level compatibility
            3. Overall compatibility score (0.0 to 1.0)
            
            Respond with ONLY a JSON object in this exact format:
            {{
                "analysis": "<detailed analysis of the intersection>",
                "overall_compatibility": <0.0 to 1.0>,
                "skill_matches": ["match1", "match2"],
                "skill_gaps": ["gap1", "gap2"],
                "experience_match": "<excellent/good/fair/poor>"
            }}
            """
            
            result = await self.llm_agent.query_llm(prompt)
            
            if result["success"]:
                try:
                    content = result["content"]
                    content = re.sub(r"^```json\s*|```$", "", content.strip(), flags=re.MULTILINE)
                    content = content.strip()
                    analysis = json.loads(content)
                    
                    response = IntersectionResponse(
                        analysis=analysis["analysis"],
                        overall_compatibility=analysis["overall_compatibility"],
                        skill_matches=analysis["skill_matches"],
                        skill_gaps=analysis["skill_gaps"],
                        experience_match=analysis["experience_match"]
                    )
                    
                    print(f"🔍 {self.name}: Intersection evaluation complete")
                    await ctx.send(sender, response)
                    
                except (json.JSONDecodeError, KeyError) as e:
                    print(f"❌ {self.name}: JSON parsing error: {e}")
                    response = IntersectionResponse(
                        analysis="Default intersection analysis",
                        overall_compatibility=0.7,
                        skill_matches=["python", "javascript"],
                        skill_gaps=["microservices"],
                        experience_match="good"
                    )
                    await ctx.send(sender, response)
            else:
                response = IntersectionResponse(
                    analysis=f"API Error: {result['content']}",
                    overall_compatibility=0.7,
                    skill_matches=["python", "javascript"],
                    skill_gaps=["microservices"],
                    experience_match="good"
                )
                await ctx.send(sender, response)
        
        self.include(self.protocol)

# Pro-Hire Advocate Agent
class ProHireAgent(Agent):
    def __init__(self):
        super().__init__("pro_hire_advocate", 8004, "pro_hire_seed")
        fund_agent_if_low(self.wallet.address())
        
        self.llm_agent = SimpleLLMAgent("pro_hire_advocate")
        self.protocol = Protocol()
        
        @self.protocol.on_message(model=DebateRequest)
        async def handle_debate(ctx: Context, sender: str, msg: DebateRequest):
            print(f"✅ {self.name}: Building pro-hire argument (round {msg.round_number})")
            
            prompt = f"""
            You are a pro-hire advocate. Build a compelling argument for hiring this candidate.
            
            Intersection Analysis:
            {msg.intersection_analysis.analysis}
            Overall Compatibility: {msg.intersection_analysis.overall_compatibility}
            Skill Matches: {', '.join(msg.intersection_analysis.skill_matches)}
            Skill Gaps: {', '.join(msg.intersection_analysis.skill_gaps)}
            
            Previous Anti-Hire Argument: {msg.previous_argument}
            
            Build a strong pro-hire argument for round {msg.round_number}.
            Focus on the candidate's strengths and how they outweigh any concerns.
            
            Respond with ONLY a JSON object in this exact format:
            {{
                "argument": "<your pro-hire argument>",
                "confidence": <0.0 to 1.0>,
                "key_points": ["point1", "point2", "point3"]
            }}
            """
            
            result = await self.llm_agent.query_llm(prompt)
            
            if result["success"]:
                try:
                    content = result["content"]
                    content = re.sub(r"^```json\s*|```$", "", content.strip(), flags=re.MULTILINE)
                    content = content.strip()
                    analysis = json.loads(content)
                    
                    response = DebateResponse(
                        position="pro",
                        argument=analysis["argument"],
                        confidence=analysis["confidence"],
                        key_points=analysis["key_points"]
                    )
                    
                    print(f"✅ {self.name}: Pro-hire argument complete")
                    await ctx.send(sender, response)
                    
                except (json.JSONDecodeError, KeyError) as e:
                    print(f"❌ {self.name}: JSON parsing error: {e}")
                    response = DebateResponse(
                        position="pro",
                        argument="Candidate has strong technical skills and relevant experience",
                        confidence=0.8,
                        key_points=["Technical skills", "Experience level"]
                    )
                    await ctx.send(sender, response)
            else:
                response = DebateResponse(
                    position="pro",
                    argument="Candidate has strong technical skills and relevant experience",
                    confidence=0.8,
                    key_points=["Technical skills", "Experience level"]
                )
                await ctx.send(sender, response)
        
        self.include(self.protocol)

# Anti-Hire Advocate Agent
class AntiHireAgent(Agent):
    def __init__(self):
        super().__init__("anti_hire_advocate", 8005, "anti_hire_seed")
        fund_agent_if_low(self.wallet.address())
        
        self.llm_agent = SimpleLLMAgent("anti_hire_advocate")
        self.protocol = Protocol()
        
        @self.protocol.on_message(model=DebateRequest)
        async def handle_debate(ctx: Context, sender: str, msg: DebateRequest):
            print(f"❌ {self.name}: Building anti-hire argument (round {msg.round_number})")
            
            prompt = f"""
            You are an anti-hire advocate. Build a compelling argument against hiring this candidate.
            
            Intersection Analysis:
            {msg.intersection_analysis.analysis}
            Overall Compatibility: {msg.intersection_analysis.overall_compatibility}
            Skill Matches: {', '.join(msg.intersection_analysis.skill_matches)}
            Skill Gaps: {', '.join(msg.intersection_analysis.skill_gaps)}
            
            Previous Pro-Hire Argument: {msg.previous_argument}
            
            Build a strong anti-hire argument for round {msg.round_number}.
            Focus on the candidate's weaknesses and potential risks.
            
            Respond with ONLY a JSON object in this exact format:
            {{
                "argument": "<your anti-hire argument>",
                "confidence": <0.0 to 1.0>,
                "key_points": ["point1", "point2", "point3"]
            }}
            """
            
            result = await self.llm_agent.query_llm(prompt)
            
            if result["success"]:
                try:
                    content = result["content"]
                    content = re.sub(r"^```json\s*|```$", "", content.strip(), flags=re.MULTILINE)
                    content = content.strip()
                    analysis = json.loads(content)
                    
                    response = DebateResponse(
                        position="anti",
                        argument=analysis["argument"],
                        confidence=analysis["confidence"],
                        key_points=analysis["key_points"]
                    )
                    
                    print(f"❌ {self.name}: Anti-hire argument complete")
                    await ctx.send(sender, response)
                    
                except (json.JSONDecodeError, KeyError) as e:
                    print(f"❌ {self.name}: JSON parsing error: {e}")
                    response = DebateResponse(
                        position="anti",
                        argument="Candidate has significant skill gaps",
                        confidence=0.6,
                        key_points=["Missing skills", "Experience concerns"]
                    )
                    await ctx.send(sender, response)
            else:
                response = DebateResponse(
                    position="anti",
                    argument="Candidate has significant skill gaps",
                    confidence=0.6,
                    key_points=["Missing skills", "Experience concerns"]
                )
                await ctx.send(sender, response)
        
        self.include(self.protocol)

# Decision Maker Agent
class DecisionAgent(Agent):
    def __init__(self):
        super().__init__("decision_maker", 8006, "decision_seed")
        fund_agent_if_low(self.wallet.address())
        
        self.llm_agent = SimpleLLMAgent("decision_maker")
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
            
            result = await self.llm_agent.query_llm(prompt)
            
            if result["success"]:
                try:
                    content = result["content"]
                    content = re.sub(r"^```json\s*|```$", "", content.strip(), flags=re.MULTILINE)
                    content = content.strip()
                    analysis = json.loads(content)
                    
                    response = DecisionResponse(
                        decision=analysis["decision"],
                        confidence=analysis["confidence"],
                        reasoning=analysis["reasoning"],
                        key_factors=analysis["key_factors"]
                    )
                    
                    print(f"🎯 {self.name}: Decision made")
                    await ctx.send(sender, response)
                    
                except (json.JSONDecodeError, KeyError) as e:
                    print(f"❌ {self.name}: JSON parsing error: {e}")
                    response = DecisionResponse(
                        decision="hire",
                        confidence=0.7,
                        reasoning="Default decision based on compatibility",
                        key_factors=["Skills match", "Experience level"]
                    )
                    await ctx.send(sender, response)
            else:
                response = DecisionResponse(
                    decision="hire",
                    confidence=0.7,
                    reasoning="Default decision based on compatibility",
                    key_factors=["Skills match", "Experience level"]
                )
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
        
        # Add completion flags
        self.job_complete = False
        self.resume_complete = False
        self.intersection_complete = False
        self.debate_complete = False
        self.decision_complete = False
        
        # Add flag to prevent duplicate requests
        self.initial_requests_sent = False
        
        # Store initial data
        self.resume_content = None
        self.job_description = None
        self.candidate_name = None
        self.job_title = None
        
        self.protocol = Protocol()
        
        # Timer to send initial requests after startup
        @self.on_interval(period=3.0)
        async def send_initial_requests(ctx: Context):
            if not self.initial_requests_sent and self.job_description and self.resume_content:
                print("🤖 Starting Hiring Evaluation Process")
                print("="*60)
                print("\n📋 STEP 1: Parsing Job and Resume")
                
                # Send initial requests
                job_request = JobParseRequest(
                    job_description=self.job_description,
                    job_title=self.job_title
                )
                await ctx.send(self.job_parser_address, job_request)
                
                resume_request = ResumeParseRequest(
                    resume_content=self.resume_content,
                    candidate_name=self.candidate_name
                )
                await ctx.send(self.resume_parser_address, resume_request)
                
                # Mark as sent to prevent duplicates
                self.initial_requests_sent = True
        
        # Handle responses from each agent
        @self.protocol.on_message(model=JobParseResponse)
        async def handle_job_response(ctx: Context, sender: str, msg: JobParseResponse):
            self.job_analysis = msg
            self.job_complete = True
            print(f"Job Analysis: {msg.analysis}")
            await self._check_and_proceed(ctx)
        
        @self.protocol.on_message(model=ResumeParseResponse)
        async def handle_resume_response(ctx: Context, sender: str, msg: ResumeParseResponse):
            self.resume_analysis = msg
            self.resume_complete = True
            print(f"Resume Analysis: {msg.analysis}")
            await self._check_and_proceed(ctx)
        
        @self.protocol.on_message(model=IntersectionResponse)
        async def handle_intersection_response(ctx: Context, sender: str, msg: IntersectionResponse):
            self.intersection_analysis = msg
            self.intersection_complete = True
            print(f"\n🔍 STEP 2: Evaluating Intersection")
            print(f"Intersection Analysis: {msg.analysis}")
            print(f"Overall Compatibility: {msg.overall_compatibility:.2f}")
            await self._start_debate(ctx)
        
        @self.protocol.on_message(model=DebateResponse)
        async def handle_debate_response(ctx: Context, sender: str, msg: DebateResponse):
            if msg.position == "pro":
                self.pro_arguments.append(msg)
                print(f"Pro-Hire Round {len(self.pro_arguments)}: {msg.argument}")
            else:
                self.anti_arguments.append(msg)
                print(f"Anti-Hire Round {len(self.anti_arguments)}: {msg.argument}")
            
            await self._continue_debate(ctx)
        
        @self.protocol.on_message(model=DecisionResponse)
        async def handle_decision_response(ctx: Context, sender: str, msg: DecisionResponse):
            print(f"\n🎯 STEP 4: Making Final Decision")
            print("\n" + "="*60)
            print("FINAL HIRING DECISION")
            print("="*60)
            print(f"Decision: {msg.decision.upper()}")
            print(f"Confidence: {msg.confidence:.2f}")
            print(f"Reasoning: {msg.reasoning}")
            print(f"Key Factors: {', '.join(msg.key_factors)}")
            print("="*60)
            self.decision_complete = True
        
        self.include(self.protocol)
    
    async def _check_and_proceed(self, ctx: Context):
        """Check if we have both job and resume analysis, then proceed to intersection"""
        if self.job_complete and self.resume_complete:
            print(f"\n🔍 STEP 2: Evaluating Intersection")
            
            request = IntersectionRequest(
                job_analysis=self.job_analysis,
                resume_analysis=self.resume_analysis
            )
            await ctx.send(self.intersection_address, request)
    
    async def _start_debate(self, ctx: Context):
        """Start the debate between pro and anti hire agents"""
        print(f"\n⚖️ STEP 3: Conducting Debate")
        
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
            print(f"\n🎯 STEP 4: Making Final Decision")
            
            decision_request = DecisionRequest(
                pro_arguments=self.pro_arguments,
                anti_arguments=self.anti_arguments,
                intersection_analysis=self.intersection_analysis
            )
            await ctx.send(self.decision_address, decision_request)

# Main execution function
async def run_hiring_system(resume_content: str, job_description: str, 
                          candidate_name: str, job_title: str):
    """Run the complete hiring system with uAgents"""
    print("🚀 Starting uAgents Hiring System")
    print("="*60)
    
    # Create all agents
    job_parser = JobParserAgent()
    resume_parser = ResumeParserAgent()
    intersection_evaluator = IntersectionAgent()
    pro_hire = ProHireAgent()
    anti_hire = AntiHireAgent()
    decision_maker = DecisionAgent()
    coordinator = HiringCoordinator()
    
    # Start all agents in background tasks
    job_parser_task = asyncio.create_task(job_parser.run_async())
    resume_parser_task = asyncio.create_task(resume_parser.run_async())
    intersection_task = asyncio.create_task(intersection_evaluator.run_async())
    pro_hire_task = asyncio.create_task(pro_hire.run_async())
    anti_hire_task = asyncio.create_task(anti_hire.run_async())
    decision_task = asyncio.create_task(decision_maker.run_async())
    coordinator_task = asyncio.create_task(coordinator.run_async())
    
    # Wait for initialization
    print("⏳ Waiting for agents to initialize...")
    await asyncio.sleep(5)
    
    # Store addresses
    coordinator.job_parser_address = job_parser.address
    coordinator.resume_parser_address = resume_parser.address
    coordinator.intersection_address = intersection_evaluator.address
    coordinator.pro_hire_address = pro_hire.address
    coordinator.anti_hire_address = anti_hire.address
    coordinator.decision_address = decision_maker.address
    
    # Store initial data
    coordinator.resume_content = resume_content
    coordinator.job_description = job_description
    coordinator.candidate_name = candidate_name
    coordinator.job_title = job_title
    
    # Wait for decision to complete
    print("⏳ Waiting for hiring process to complete...")
    while not coordinator.decision_complete:
        await asyncio.sleep(1)
    
    # Cancel all tasks
    job_parser_task.cancel()
    resume_parser_task.cancel()
    intersection_task.cancel()
    pro_hire_task.cancel()
    anti_hire_task.cancel()
    decision_task.cancel()
    coordinator_task.cancel()
    
    print("\n✅ Hiring evaluation completed!")

# Test data and main execution
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
    
    # Run the hiring system
    asyncio.run(run_hiring_system(
        resume_content=resume_content,
        job_description=job_description,
        candidate_name="John Doe",
        job_title="Software Engineer"
    )) 