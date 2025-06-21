"""
Simple Hiring Agent Demo
========================

A simplified demonstration of the hiring agent system using ASI:One LLM.
This version shows the agent logic and prompts without the full uAgents complexity.
"""

import asyncio
import json
import aiohttp
import ssl
import re
from typing import List, Dict

# ASI:One API configuration
ASI_API_KEY = "sk_d1a256183aa249f49f49d649dddff42ca039df035fb7404394efe289149d9997"
ASI_API_URL = "https://api.asi1.ai/v1/chat/completions"

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
            print(f"🔗 {self.name}: Attempting API call to {self.api_url}")
            print(f"🔑 {self.name}: Using API key: {self.api_key[:20]}...")
            
            # Create SSL context to bypass certificate verification
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            connector = aiohttp.TCPConnector(ssl=ssl_context)
            
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.post(self.api_url, headers=headers, json=payload, timeout=30) as response:
                    print(f"📡 {self.name}: Response status: {response.status}")
                    
                    if response.status == 200:
                        result = await response.json()
                        #print("🔍 FULL API RESPONSE:", result)
                        return {
                            "success": True,
                            "content": result["choices"][0]["message"]["content"]
                        }
                    else:
                        error_text = await response.text()
                        print(f"❌ {self.name}: API Error {response.status}: {error_text}")
                        return {
                            "success": False,
                            "content": f"API Error {response.status}: {error_text}"
                        }
        except aiohttp.ClientConnectorError as e:
            print(f"🔌 {self.name}: Connection Error: {e}")
            return {
                "success": False,
                "content": f"Connection Error: {str(e)}"
            }
        except asyncio.TimeoutError:
            print(f"⏰ {self.name}: Request timeout")
            return {
                "success": False,
                "content": "Request timeout"
            }
        except Exception as e:
            print(f"💥 {self.name}: Unexpected error: {e}")
            return {
                "success": False,
                "content": f"Request Error: {str(e)}"
            }

class JobParserAgent(SimpleLLMAgent):
    """Agent that parses job descriptions using LLM"""
    
    def __init__(self):
        super().__init__("job_parser")
    
    async def parse_job(self, job_description: str, job_title: str) -> dict:
        print(f"💼 {self.name}: Parsing job description for {job_title}")
        
        prompt = f"""
        Analyze the following job description and extract key information.
        
        Job Title: {job_title}
        Job Description:
        {job_description}
        
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
                content = result["content"]
                # Remove markdown code block (```json ... ```)
                content = re.sub(r"^```json\s*|```$", "", content.strip(), flags=re.MULTILINE)
                content = content.strip()
                analysis = json.loads(content)
                return {
                    "job_title": job_title,
                    "required_skills": analysis["required_skills"],
                    "preferred_skills": analysis["preferred_skills"],
                    "experience_level": analysis["experience_level"],
                    "key_requirements": analysis["key_requirements"],
                    "analysis": analysis["analysis"]
                }
            except (json.JSONDecodeError, KeyError) as e:
                print(f"❌ {self.name}: JSON parsing error: {e}")
                print(f"📄 {self.name}: Raw content: {result['content']}")
                return {
                    "job_title": job_title,
                    "required_skills": ["python", "javascript"],
                    "preferred_skills": ["react"],
                    "experience_level": "Mid-level",
                    "key_requirements": ["web development"],
                    "analysis": "Failed to parse LLM response, using defaults"
                }
        else:
            return {
                "job_title": job_title,
                "required_skills": ["python", "javascript"],
                "preferred_skills": ["react"],
                "experience_level": "Mid-level",
                "key_requirements": ["web development"],
                "analysis": f"API Error: {result['content']}"
            }

class ResumeParserAgent(SimpleLLMAgent):
    """Agent that parses resumes using LLM"""
    
    def __init__(self):
        super().__init__("resume_parser")
    
    async def parse_resume(self, resume_content: str, candidate_name: str) -> dict:
        print(f"📄 {self.name}: Parsing resume for {candidate_name}")
        
        prompt = f"""
        Analyze the following resume and extract key information.
        
        Candidate Name: {candidate_name}
        Resume Content:
        {resume_content}
        
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
                content = result["content"]
                # Remove markdown code block (```json ... ```)
                content = re.sub(r"^```json\s*|```$", "", content.strip(), flags=re.MULTILINE)
                content = content.strip()
                analysis = json.loads(content)
                return {
                    "candidate_name": candidate_name,
                    "skills": analysis["skills"],
                    "experience_years": analysis["experience_years"],
                    "experience_level": analysis["experience_level"],
                    "key_achievements": analysis["key_achievements"],
                    "analysis": analysis["analysis"]
                }
            except (json.JSONDecodeError, KeyError) as e:
                print(f"❌ {self.name}: JSON parsing error: {e}")
                print(f"📄 {self.name}: Raw content: {result['content']}")
                return {
                    "candidate_name": candidate_name,
                    "skills": ["python", "javascript"],
                    "experience_years": 2,
                    "experience_level": "Mid-level",
                    "key_achievements": ["web development"],
                    "analysis": "Failed to parse LLM response, using defaults"
                }
        else:
            return {
                "candidate_name": candidate_name,
                "skills": ["python", "javascript"],
                "experience_years": 2,
                "experience_level": "Mid-level",
                "key_achievements": ["web development"],
                "analysis": f"API Error: {result['content']}"
            }

class IntersectionAgent(SimpleLLMAgent):
    """Agent that finds intersection between job and resume"""
    
    def __init__(self):
        super().__init__("intersection_evaluator")
    
    async def evaluate_intersection(self, job_analysis: dict, resume_analysis: dict) -> dict:
        print(f"🔍 {self.name}: Evaluating intersection")
        
        prompt = f"""
        Analyze the intersection between the job requirements and candidate profile.
        
        Job Analysis:
        {job_analysis['analysis']}
        Required Skills: {job_analysis['required_skills']}
        Preferred Skills: {job_analysis['preferred_skills']}
        Experience Level: {job_analysis['experience_level']}
        
        Candidate Analysis:
        {resume_analysis['analysis']}
        Skills: {resume_analysis['skills']}
        Experience: {resume_analysis['experience_years']} years ({resume_analysis['experience_level']})
        Achievements: {resume_analysis['key_achievements']}
        
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
                content = result["content"]
                # Remove markdown code block (```json ... ```)
                content = re.sub(r"^```json\s*|```$", "", content.strip(), flags=re.MULTILINE)
                content = content.strip()
                analysis = json.loads(content)
                return {
                    "matching_skills": analysis["matching_skills"],
                    "missing_skills": analysis["missing_skills"],
                    "experience_match": analysis["experience_match"],
                    "overall_compatibility": analysis["overall_compatibility"],
                    "strengths": analysis["strengths"],
                    "weaknesses": analysis["weaknesses"],
                    "analysis": analysis["analysis"]
                }
            except (json.JSONDecodeError, KeyError) as e:
                print(f"❌ {self.name}: JSON parsing error: {e}")
                print(f"📄 {self.name}: Raw content: {result['content']}")
                return {
                    "matching_skills": ["python", "javascript"],
                    "missing_skills": [],
                    "experience_match": True,
                    "overall_compatibility": 0.7,
                    "strengths": ["Good technical skills"],
                    "weaknesses": [],
                    "analysis": "Failed to parse LLM response, using defaults"
                }
        else:
            return {
                "matching_skills": ["python", "javascript"],
                "missing_skills": [],
                "experience_match": True,
                "overall_compatibility": 0.7,
                "strengths": ["Good technical skills"],
                "weaknesses": [],
                "analysis": f"API Error: {result['content']}"
            }

class ProHireAgent(SimpleLLMAgent):
    """Agent that advocates for hiring"""
    
    def __init__(self):
        super().__init__("pro_hire_advocate")
    
    async def build_argument(self, intersection_analysis: dict, round_number: int, previous_argument: str = "") -> dict:
        print(f"✅ {self.name}: Building pro-hire argument (round {round_number})")
        
        context = f"Previous argument: {previous_argument}" if previous_argument else "First round of debate"
        
        prompt = f"""
        You are advocating FOR hiring this candidate. Build a compelling argument based on the intersection analysis.
        
        Intersection Analysis:
        {intersection_analysis['analysis']}
        Matching Skills: {intersection_analysis['matching_skills']}
        Strengths: {intersection_analysis['strengths']}
        Overall Compatibility: {intersection_analysis['overall_compatibility']}
        
        Context: {context}
        Round: {round_number}
        
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
                content = result["content"]
                # Remove markdown code block (```json ... ```)
                content = re.sub(r"^```json\s*|```$", "", content.strip(), flags=re.MULTILINE)
                content = content.strip()
                analysis = json.loads(content)
                return {
                    "position": "pro",
                    "argument": analysis["argument"],
                    "confidence": analysis["confidence"],
                    "key_points": analysis["key_points"]
                }
            except (json.JSONDecodeError, KeyError) as e:
                print(f"❌ {self.name}: JSON parsing error: {e}")
                print(f"📄 {self.name}: Raw content: {result['content']}")
                return {
                    "position": "pro",
                    "argument": "Candidate shows good potential and matching skills",
                    "confidence": 0.7,
                    "key_points": ["Good skills match", "Potential for growth"]
                }
        else:
            return {
                "position": "pro",
                "argument": "Candidate shows good potential and matching skills",
                "confidence": 0.7,
                "key_points": ["Good skills match", "Potential for growth"]
            }

class AntiHireAgent(SimpleLLMAgent):
    """Agent that advocates against hiring"""
    
    def __init__(self):
        super().__init__("anti_hire_advocate")
    
    async def build_argument(self, intersection_analysis: dict, round_number: int, previous_argument: str = "") -> dict:
        print(f"❌ {self.name}: Building anti-hire argument (round {round_number})")
        
        context = f"Previous argument: {previous_argument}" if previous_argument else "First round of debate"
        
        prompt = f"""
        You are advocating AGAINST hiring this candidate. Build a compelling argument based on the intersection analysis.
        
        Intersection Analysis:
        {intersection_analysis['analysis']}
        Missing Skills: {intersection_analysis['missing_skills']}
        Weaknesses: {intersection_analysis['weaknesses']}
        Overall Compatibility: {intersection_analysis['overall_compatibility']}
        
        Context: {context}
        Round: {round_number}
        
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
                content = result["content"]
                # Remove markdown code block (```json ... ```)
                content = re.sub(r"^```json\s*|```$", "", content.strip(), flags=re.MULTILINE)
                content = content.strip()
                analysis = json.loads(content)
                return {
                    "position": "anti",
                    "argument": analysis["argument"],
                    "confidence": analysis["confidence"],
                    "key_points": analysis["key_points"]
                }
            except (json.JSONDecodeError, KeyError) as e:
                print(f"❌ {self.name}: JSON parsing error: {e}")
                print(f"📄 {self.name}: Raw content: {result['content']}")
                return {
                    "position": "anti",
                    "argument": "Candidate has significant skill gaps",
                    "confidence": 0.6,
                    "key_points": ["Missing skills", "Experience concerns"]
                }
        else:
            return {
                "position": "anti",
                "argument": "Candidate has significant skill gaps",
                "confidence": 0.6,
                "key_points": ["Missing skills", "Experience concerns"]
            }

class DecisionAgent(SimpleLLMAgent):
    """Agent that makes the final hiring decision"""
    
    def __init__(self):
        super().__init__("decision_maker")
    
    async def make_decision(self, pro_arguments: List[dict], anti_arguments: List[dict], intersection_analysis: dict) -> dict:
        print(f"🎯 {self.name}: Making final hiring decision")
        
        # Format debate arguments for the prompt
        pro_args = "\n".join([f"Round {i+1}: {arg['argument']}" for i, arg in enumerate(pro_arguments)])
        anti_args = "\n".join([f"Round {i+1}: {arg['argument']}" for i, arg in enumerate(anti_arguments)])
        
        prompt = f"""
        You are the final decision maker for a hiring decision. Evaluate all the arguments and make a final decision.
        
        Intersection Analysis:
        {intersection_analysis['analysis']}
        Overall Compatibility: {intersection_analysis['overall_compatibility']}
        
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
                content = result["content"]
                # Remove markdown code block (```json ... ```)
                content = re.sub(r"^```json\s*|```$", "", content.strip(), flags=re.MULTILINE)
                content = content.strip()
                analysis = json.loads(content)
                return {
                    "decision": analysis["decision"],
                    "confidence": analysis["confidence"],
                    "reasoning": analysis["reasoning"],
                    "key_factors": analysis["key_factors"]
                }
            except (json.JSONDecodeError, KeyError) as e:
                print(f"❌ {self.name}: JSON parsing error: {e}")
                print(f"📄 {self.name}: Raw content: {result['content']}")
                return {
                    "decision": "hire",
                    "confidence": 0.7,
                    "reasoning": "Default decision based on compatibility",
                    "key_factors": ["Skills match", "Experience level"]
                }
        else:
            return {
                "decision": "hire",
                "confidence": 0.7,
                "reasoning": "Default decision based on compatibility",
                "key_factors": ["Skills match", "Experience level"]
            }

class HiringCoordinator:
    """Coordinates the hiring process"""
    
    def __init__(self):
        self.job_parser = JobParserAgent()
        self.resume_parser = ResumeParserAgent()
        self.intersection_evaluator = IntersectionAgent()
        self.pro_hire = ProHireAgent()
        self.anti_hire = AntiHireAgent()
        self.decision_maker = DecisionAgent()
    
    async def evaluate_candidate(self, resume_content: str, job_description: str, 
                               candidate_name: str, job_title: str) -> dict:
        """Run the complete hiring evaluation process"""
        print("🤖 Starting Hiring Evaluation Process")
        print("="*60)
        
        # Step 1: Parse job and resume
        print("\n📋 STEP 1: Parsing Job and Resume")
        job_analysis = await self.job_parser.parse_job(job_description, job_title)
        resume_analysis = await self.resume_parser.parse_resume(resume_content, candidate_name)
        
        print(f"Job Analysis: {job_analysis['analysis']}")
        print(f"Resume Analysis: {resume_analysis['analysis']}")
        
        # Step 2: Evaluate intersection
        print("\n🔍 STEP 2: Evaluating Intersection")
        intersection_analysis = await self.intersection_evaluator.evaluate_intersection(job_analysis, resume_analysis)
        
        print(f"Intersection Analysis: {intersection_analysis['analysis']}")
        print(f"Overall Compatibility: {intersection_analysis['overall_compatibility']:.2f}")
        
        # Step 3: Conduct debate
        print("\n⚖️ STEP 3: Conducting Debate")
        pro_arguments = []
        anti_arguments = []
        
        for round_num in range(1, 4):  # 3 rounds each
            # Pro-hire argument
            pro_arg = await self.pro_hire.build_argument(
                intersection_analysis, 
                round_num,
                anti_arguments[-1]['argument'] if anti_arguments else ""
            )
            pro_arguments.append(pro_arg)
            print(f"Pro-Hire Round {round_num}: {pro_arg['argument'][:100]}...")
            
            # Anti-hire argument
            anti_arg = await self.anti_hire.build_argument(
                intersection_analysis,
                round_num,
                pro_arg['argument']
            )
            anti_arguments.append(anti_arg)
            print(f"Anti-Hire Round {round_num}: {anti_arg['argument'][:100]}...")
        
        # Step 4: Make final decision
        print("\n🎯 STEP 4: Making Final Decision")
        final_decision = await self.decision_maker.make_decision(
            pro_arguments, anti_arguments, intersection_analysis
        )
        
        # Display results
        print("\n" + "="*60)
        print("FINAL HIRING DECISION")
        print("="*60)
        print(f"Decision: {final_decision['decision'].upper()}")
        print(f"Confidence: {final_decision['confidence']:.2f}")
        print(f"Reasoning: {final_decision['reasoning']}")
        print(f"Key Factors: {', '.join(final_decision['key_factors'])}")
        print("="*60)
        
        return {
            "decision": final_decision,
            "job_analysis": job_analysis,
            "resume_analysis": resume_analysis,
            "intersection_analysis": intersection_analysis,
            "pro_arguments": pro_arguments,
            "anti_arguments": anti_arguments
        }

async def main():
    """Main function to run the hiring system"""
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
    coordinator = HiringCoordinator()
    result = await coordinator.evaluate_candidate(
        resume_content=resume_content,
        job_description=job_description,
        candidate_name="John Doe",
        job_title="Software Engineer"
    )
    
    print("\n✅ Hiring evaluation completed!")

if __name__ == "__main__":
    asyncio.run(main()) 