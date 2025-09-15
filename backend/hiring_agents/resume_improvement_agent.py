"""
Resume Improvement Agent
=======================

This agent analyzes student resumes and provides educational feedback
for career development in specific fields.
"""
#Boilder plate code for the resume improvement agent
#Will update this to be more specific to the field of intrest
#How I want it, is I input my major and it gives me some fields
import json
from typing import Dict, List, Optional
from .llm_client import SimpleLLMAgent


class ResumeImprovementAgent(SimpleLLMAgent):
    """Agent that provides educational resume feedback for students"""

    def __init__(self):
        super().__init__("resume_improvement_agent")

        # Generic job templates for different fields across all engineering disciplines
        self.field_templates = {
            # Computer Science Fields
            "frontend": {
                "title": "Frontend Developer",
                "key_skills": [
                    "React",
                    "JavaScript",
                    "HTML/CSS",
                    "TypeScript",
                    "Vue.js",
                    "Angular",
                    "Git",
                    "UI/UX",
                ],
                "projects": [
                    "Portfolio website",
                    "E-commerce frontend",
                    "Dashboard interface",
                    "Mobile-responsive app",
                ],
                "description": "Develop user-facing web applications using modern JavaScript frameworks",
            },
            "backend": {
                "title": "Backend Developer",
                "key_skills": [
                    "Python",
                    "Node.js",
                    "Java",
                    "SQL",
                    "REST APIs",
                    "Database Design",
                    "Git",
                    "Cloud", 
                ],
                "projects": [
                    "REST API service",
                    "Database-driven application",
                    "Microservices architecture",
                    "Authentication system",
                ],
                "description": "Build server-side applications, APIs, and database systems",
            },
            "fullstack": {
                "title": "Full Stack Developer",
                "key_skills": [
                    "JavaScript",
                    "Python",
                    "React",
                    "Node.js",
                    "SQL",
                    "Git",
                    "AWS",
                    "Docker",
                ],
                "projects": [
                    "Full-stack web application",
                    "CRUD application with database",
                    "Real-time chat app",
                    "E-commerce platform",
                ],
                "description": "Develop both frontend and backend components of web applications",
            },
            "devops": {
                "title": "DevOps Engineer",
                "key_skills": [
                    "Docker",
                    "Kubernetes",
                    "AWS",
                    "Jenkins",
                    "Git",
                    "Linux",
                    "CI/CD",
                    "Infrastructure",
                ],
                "projects": [
                    "CI/CD pipeline setup",
                    "Infrastructure as Code",
                    "Container orchestration",
                    "Monitoring dashboard",
                ],
                "description": "Automate deployment processes and manage cloud infrastructure",
            },
            "data-science": {
                "title": "Data Scientist",
                "key_skills": [
                    "Python",
                    "Machine Learning",
                    "SQL",
                    "Statistics",
                    "AI",
                    "Deep Learning",
                    "Pandas",
                    "NumPy",
                ],
                "projects": [
                    "Predictive modeling project",
                    "Data visualization dashboard",
                    "Machine learning classifier",
                    "AI application",
                ],
                "description": "Analyze data to extract insights and build AI/ML models",
            },
            # Electrical Engineering Fields
            "embedded": {
                "title": "Embedded Systems Engineer",
                "key_skills": [
                    "C/C++",
                    "Microcontrollers",
                    "RTOS",
                    "IoT",
                    "Firmware",
                    "Hardware",
                    "Sensors",
                ],
                "projects": [
                    "IoT sensor network",
                    "Microcontroller-based system",
                    "Real-time control system",
                    "Embedded firmware",
                ],
                "description": "Develop software for embedded hardware systems and IoT devices",
            },
            "power-systems": {
                "title": "Power Systems Engineer",
                "key_skills": [
                    "Power Electronics",
                    "Smart Grids",
                    "Renewable Energy",
                    "MATLAB",
                    "Control Systems",
                    "Power Analysis",
                ],
                "projects": [
                    "Smart grid simulation",
                    "Renewable energy system",
                    "Power quality analysis",
                    "Grid automation project",
                ],
                "description": "Design and optimize electrical power generation and distribution systems",
            },
            "signal-processing": {
                "title": "Signal Processing Engineer",
                "key_skills": [
                    "DSP",
                    "MATLAB",
                    "Python",
                    "Communications",
                    "5G/6G",
                    "RF Engineering",
                    "Wireless",
                ],
                "projects": [
                    "Digital filter design",
                    "Communication system simulation",
                    "Signal analysis tool",
                    "Wireless protocol implementation",
                ],
                "description": "Design and implement digital signal processing and communication systems",
            },
            "control-systems": {
                "title": "Control Systems Engineer",
                "key_skills": [
                    "Control Theory",
                    "PLC Programming",
                    "SCADA",
                    "Industrial Automation",
                    "Robotics",
                    "MATLAB",
                ],
                "projects": [
                    "Automated control system",
                    "PLC programming project",
                    "Robotics control",
                    "Process automation",
                ],
                "description": "Design automated control systems for industrial and robotics applications",
            },
            "vlsi": {
                "title": "VLSI Design Engineer",
                "key_skills": [
                    "Verilog",
                    "VHDL",
                    "IC Design",
                    "Hardware Verification",
                    "Digital Design",
                    "CAD Tools",
                ],
                "projects": [
                    "Digital circuit design",
                    "FPGA implementation",
                    "IC verification project",
                    "Hardware accelerator",
                ],
                "description": "Design and verify integrated circuits and digital hardware systems",
            },
            # Mechanical Engineering Fields
            "robotics": {
                "title": "Robotics Engineer",
                "key_skills": [
                    "ROS",
                    "Python",
                    "C++",
                    "Control Systems",
                    "AI Integration",
                    "CAD",
                    "Sensors",
                ],
                "projects": [
                    "Autonomous robot",
                    "Robotic arm control",
                    "Computer vision robot",
                    "Industrial automation",
                ],
                "description": "Design and program robots for industrial and consumer applications",
            },
            "automotive": {
                "title": "Automotive Engineer",
                "key_skills": [
                    "CAD",
                    "MATLAB",
                    "Testing",
                    "Electric Vehicles",
                    "Autonomous Systems",
                    "Automotive Standards",
                ],
                "projects": [
                    "Vehicle component design",
                    "EV powertrain analysis",
                    "Autonomous driving feature",
                    "Crash simulation",
                ],
                "description": "Design and test automotive systems including electric and autonomous vehicles",
            },
            "aerospace": {
                "title": "Aerospace Engineer",
                "key_skills": [
                    "CAD",
                    "MATLAB",
                    "CFD",
                    "Propulsion",
                    "Flight Dynamics",
                    "Space Systems",
                ],
                "projects": [
                    "Aircraft component design",
                    "Propulsion system analysis",
                    "Flight simulation",
                    "Satellite system",
                ],
                "description": "Design aircraft, spacecraft, and propulsion systems",
            },
            "manufacturing": {
                "title": "Manufacturing Engineer",
                "key_skills": [
                    "Lean Manufacturing",
                    "Six Sigma",
                    "Quality Control",
                    "Process Optimization",
                    "CAD",
                    "Automation",
                ],
                "projects": [
                    "Process improvement study",
                    "Quality control system",
                    "Manufacturing automation",
                    "Lean implementation",
                ],
                "description": "Optimize manufacturing processes and improve production efficiency",
            },
            "thermal-fluids": {
                "title": "Thermal Systems Engineer",
                "key_skills": [
                    "CFD",
                    "Heat Transfer",
                    "HVAC",
                    "Energy Systems",
                    "MATLAB",
                    "Thermodynamics",
                ],
                "projects": [
                    "HVAC system design",
                    "CFD analysis",
                    "Energy efficiency study",
                    "Thermal management",
                ],
                "description": "Design thermal and fluid systems for energy and HVAC applications",
            },
            # Civil Engineering Fields
            "structural": {
                "title": "Structural Engineer",
                "key_skills": [
                    "Structural Analysis",
                    "CAD",
                    "Steel Design",
                    "Concrete Design",
                    "Earthquake Engineering",
                    "Building Codes",
                ],
                "projects": [
                    "Building structure design",
                    "Earthquake analysis",
                    "Bridge design",
                    "Foundation analysis",
                ],
                "description": "Design safe and efficient building and infrastructure structures",
            },
            "transportation": {
                "title": "Transportation Engineer",
                "key_skills": [
                    "Traffic Engineering",
                    "Highway Design",
                    "Smart Infrastructure",
                    "Transportation Planning",
                    "GIS",
                ],
                "projects": [
                    "Traffic flow analysis",
                    "Highway design project",
                    "Smart traffic system",
                    "Transportation planning",
                ],
                "description": "Design transportation systems and smart infrastructure",
            },
            "environmental": {
                "title": "Environmental Engineer",
                "key_skills": [
                    "Water Treatment",
                    "Sustainability",
                    "Environmental Analysis",
                    "Green Infrastructure",
                    "GIS",
                ],
                "projects": [
                    "Water treatment design",
                    "Environmental impact study",
                    "Green building project",
                    "Pollution control",
                ],
                "description": "Design sustainable solutions for environmental protection",
            },
            "geotechnical": {
                "title": "Geotechnical Engineer",
                "key_skills": [
                    "Soil Mechanics",
                    "Foundation Design",
                    "Slope Stability",
                    "Ground Improvement",
                    "Site Investigation",
                ],
                "projects": [
                    "Foundation analysis",
                    "Slope stability study",
                    "Ground improvement design",
                    "Site investigation",
                ],
                "description": "Analyze soil and rock mechanics for construction projects",
            },
            "construction": {
                "title": "Construction Manager",
                "key_skills": [
                    "Project Management",
                    "BIM",
                    "Construction Technology",
                    "Scheduling",
                    "Cost Estimation",
                ],
                "projects": [
                    "BIM model development",
                    "Project scheduling",
                    "Cost estimation study",
                    "Construction planning",
                ],
                "description": "Manage construction projects using modern technology and methods",
            },
            # Chemical Engineering Fields
            "process-engineering": {
                "title": "Process Engineer",
                "key_skills": [
                    "Process Design",
                    "Chemical Processes",
                    "Plant Design",
                    "Process Optimization",
                    "MATLAB",
                    "Simulation",
                ],
                "projects": [
                    "Process flow design",
                    "Plant optimization",
                    "Chemical reactor design",
                    "Process simulation",
                ],
                "description": "Design and optimize chemical manufacturing processes",
            },
            "biotechnology": {
                "title": "Biotechnology Engineer",
                "key_skills": [
                    "Bioprocessing",
                    "Pharmaceuticals",
                    "Biomedical Engineering",
                    "Cell Culture",
                    "Bioreactors",
                ],
                "projects": [
                    "Bioprocess design",
                    "Pharmaceutical analysis",
                    "Biomedical device",
                    "Cell culture optimization",
                ],
                "description": "Apply engineering principles to biological and medical systems",
            },
            "materials": {
                "title": "Materials Engineer",
                "key_skills": [
                    "Nanomaterials",
                    "Polymers",
                    "Advanced Materials",
                    "Materials Testing",
                    "Characterization",
                ],
                "projects": [
                    "Materials synthesis",
                    "Properties testing",
                    "Nanomaterial application",
                    "Composite design",
                ],
                "description": "Develop and test new materials for various applications",
            },
            "environmental-chemical": {
                "title": "Environmental & Sustainability Engineer",
                "key_skills": [
                    "Green Chemistry",
                    "Waste Treatment",
                    "Carbon Capture",
                    "Sustainability",
                    "Life Cycle Analysis",
                ],
                "projects": [
                    "Green process design",
                    "Waste treatment system",
                    "Carbon footprint analysis",
                    "Sustainability study",
                ],
                "description": "Develop sustainable chemical processes and environmental solutions",
            },
            "energy-chemical": {
                "title": "Energy Systems Engineer",
                "key_skills": [
                    "Renewable Energy",
                    "Battery Technology",
                    "Fuel Cells",
                    "Energy Storage",
                    "Process Engineering",
                ],
                "projects": [
                    "Battery design project",
                    "Fuel cell analysis",
                    "Renewable energy system",
                    "Energy storage study",
                ],
                "description": "Design energy systems including batteries and renewable technologies",
            },
            # Industrial Engineering Fields
            "data-analytics": {
                "title": "Data Analytics & Operations Research Engineer",
                "key_skills": [
                    "Business Intelligence",
                    "Statistics",
                    "Optimization",
                    "Python",
                    "R",
                    "Data Visualization",
                ],
                "projects": [
                    "Business analytics dashboard",
                    "Optimization model",
                    "Statistical analysis",
                    "Predictive analytics",
                ],
                "description": "Use data analytics and optimization to improve business operations",
            },
            "supply-chain": {
                "title": "Supply Chain Engineer",
                "key_skills": [
                    "Logistics",
                    "Inventory Management",
                    "Global Operations",
                    "Supply Chain Analytics",
                    "ERP Systems",
                ],
                "projects": [
                    "Supply chain optimization",
                    "Inventory analysis",
                    "Logistics network design",
                    "Demand forecasting",
                ],
                "description": "Optimize supply chain and logistics operations",
            },
            "quality-engineering": {
                "title": "Quality Engineer",
                "key_skills": [
                    "Six Sigma",
                    "Statistical Process Control",
                    "Quality Systems",
                    "Lean Manufacturing",
                    "ISO Standards",
                ],
                "projects": [
                    "Quality improvement project",
                    "Six Sigma analysis",
                    "Process control system",
                    "Quality audit",
                ],
                "description": "Implement quality management systems and continuous improvement",
            },
            "human-factors": {
                "title": "Human Factors Engineer",
                "key_skills": [
                    "Ergonomics",
                    "User Experience",
                    "Safety Engineering",
                    "Human-Computer Interaction",
                    "Usability",
                ],
                "projects": [
                    "Ergonomic design study",
                    "Safety analysis",
                    "UX improvement project",
                    "Workplace design",
                ],
                "description": "Design systems that optimize human performance and safety",
            },
            "project-management": {
                "title": "Project & Systems Manager",
                "key_skills": [
                    "Project Planning",
                    "Systems Engineering",
                    "Risk Management",
                    "Agile",
                    "PMP",
                    "Leadership",
                ],
                "projects": [
                    "Project management plan",
                    "Systems design",
                    "Risk assessment",
                    "Process improvement",
                ],
                "description": "Lead complex engineering projects and systems development",
            },
        }

    async def analyze_resume_for_improvement(
        self,
        resume_content: str,
        candidate_name: str,
        field_of_interest: str,
        major: str = "Computer Science",
    ) -> Dict:
        """
        Analyze a student's resume and provide improvement recommendations
        """
        print(
            f"🎓 {self.name}: Analyzing resume for {candidate_name} interested in {field_of_interest}"
        )

        # Get field template
        field_key = (
            field_of_interest.lower()
            .replace(" ", "-")
            .replace("development", "")
            .strip()
        )
        field_template = self.field_templates.get(
            field_key, self.field_templates["backend"]
        )

        prompt = self._build_improvement_prompt(
            resume_content, candidate_name, field_of_interest, field_template, major
        )

        try:
            result = await self.query_llm(prompt)

            if result["success"]:
                analysis = self.parse_json_response(result["content"])
                if analysis:
                    print(
                        f"✅ {self.name}: Generated educational feedback for {candidate_name}"
                    )
                    return analysis
                else:
                    print(f"❌ {self.name}: Failed to parse feedback response")
                    return self._create_fallback_response(
                        candidate_name, field_of_interest, field_template
                    )
            else:
                print(f"❌ {self.name}: LLM query failed: {result['content']}")
                return self._create_fallback_response(
                    candidate_name, field_of_interest, field_template
                )

        except Exception as e:
            print(f"💥 {self.name}: Error during analysis: {e}")
            return self._create_fallback_response(
                candidate_name, field_of_interest, field_template
            )

    def _build_improvement_prompt(
        self,
        resume_content: str,
        candidate_name: str,
        field_of_interest: str,
        field_template: Dict,
        major: str,
    ) -> str:
        """Build the prompt for resume improvement analysis"""

        return f"""
You are an educational career counselor helping a {major} student improve their resume for a career in {field_of_interest}.

STUDENT INFORMATION:
- Name: {candidate_name}
- Major: {major}
- Field of Interest: {field_of_interest}
- Career Goal: {field_template['title']}

FIELD REQUIREMENTS:
- Key Skills Needed: {', '.join(field_template['key_skills'])}
- Typical Projects: {', '.join(field_template['projects'])}
- Field Description: {field_template['description']}

STUDENT'S RESUME:
{resume_content}

TASK: Analyze this student's resume and provide educational feedback to help them prepare for a career in {field_of_interest}. Be encouraging and educational - focus on growth opportunities rather than just gaps.

Provide your analysis in this exact JSON format:
{{
    "candidate_name": "{candidate_name}",
    "field_selected": "{field_of_interest}",
    "current_strengths": [
        "List specific strengths you see in their resume that are relevant to {field_of_interest}",
        "Include both technical skills and soft skills",
        "Be specific about projects, coursework, or experience that applies"
    ],
    "skill_gaps": [
        "List 3-5 key skills they should learn for {field_of_interest}",
        "Focus on the most important gaps based on the field requirements",
        "Phrase constructively (e.g., 'Would benefit from learning...' rather than 'Lacks...')"
    ],
    "recommended_skills": [
        "List 5-8 specific technical skills to prioritize learning",
        "Include both beginner and intermediate level skills",
        "Based on the field requirements and current market demands"
    ],
    "recommended_projects": [
        "Suggest 4-6 specific project ideas they could build",
        "Make them achievable for a student level",
        "Ensure projects would demonstrate the key skills needed",
        "Include brief descriptions of what each project would involve"
    ],
    "actionable_steps": [
        "Provide 5-7 specific, actionable steps they can take immediately",
        "Include learning resources, project ideas, and resume improvements",
        "Prioritize steps from most important to least important",
        "Make each step concrete and achievable"
    ],
    "overall_score": 7,
    "feedback_summary": "Write 2-3 encouraging sentences summarizing their current position and potential for growth in {field_of_interest}. Be specific about what they're doing well and what the next steps are."
}}

IMPORTANT: 
- Be encouraging and educational, not critical
- Focus on growth and learning opportunities
- Provide specific, actionable advice
- Consider this is likely a student or new graduate
- Score should be realistic but encouraging (usually 5-8 for students)
- Make recommendations specific to {field_of_interest}
"""

    def _create_fallback_response(
        self, candidate_name: str, field_of_interest: str, field_template: Dict
    ) -> Dict:
        """Create a fallback response when LLM analysis fails"""
        return {
            "candidate_name": candidate_name,
            "field_selected": field_of_interest,
            "current_strengths": [
                "Educational background in relevant field",
                "Interest in pursuing career in technology",
                "Willingness to learn and grow",
            ],
            "skill_gaps": [
                f"Would benefit from learning core {field_of_interest.lower()} technologies",
                "Could strengthen practical project experience",
                "Portfolio development would be valuable",
            ],
            "recommended_skills": field_template["key_skills"][:6],
            "recommended_projects": field_template["projects"],
            "actionable_steps": [
                f"Start learning the fundamentals of {field_of_interest.lower()}",
                "Build your first project to apply new skills",
                "Create a GitHub portfolio to showcase your work",
                "Join online communities related to your field",
                "Consider internships or part-time opportunities",
            ],
            "overall_score": 6,
            "feedback_summary": f"You're on a great path toward a career in {field_of_interest}! Focus on building practical experience through projects and developing the key technical skills employers are looking for.",
        }
