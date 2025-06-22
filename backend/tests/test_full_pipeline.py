#!/usr/bin/env python3
"""
Test Full PDF to LLM Pipeline
==============================

Test script that demonstrates the complete PDF upload and analysis pipeline.
"""

import sys
import os
import asyncio

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from hiring_agents.pdf_parser import PDFParser
from hiring_agents.llm_client import SimpleLLMAgent

async def test_full_pipeline():
    """Test the complete PDF parsing and LLM analysis pipeline."""
    print("🧪 Testing Full PDF to LLM Pipeline...")
    print("=" * 50)
    
    # Step 1: Create a test PDF
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        import io
        
        print("📄 Step 1: Creating test PDF...")
        
        # Create a more comprehensive test PDF
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        
        # Add realistic resume content
        p.drawString(100, 750, "SARAH JOHNSON")
        p.drawString(100, 730, "Senior Software Engineer")
        p.drawString(100, 710, "sarah.johnson@email.com | (555) 123-4567")
        p.drawString(100, 680, "")
        
        p.drawString(100, 650, "PROFESSIONAL SUMMARY")
        p.drawString(100, 630, "Experienced software engineer with 7+ years in full-stack development.")
        p.drawString(100, 610, "Expertise in Python, React, and cloud technologies. Led teams of 6+ engineers.")
        p.drawString(100, 590, "")
        
        p.drawString(100, 560, "TECHNICAL SKILLS")
        p.drawString(100, 540, "• Programming: Python, JavaScript, TypeScript, Java, Go")
        p.drawString(100, 520, "• Frontend: React, Vue.js, Angular, HTML5, CSS3")
        p.drawString(100, 500, "• Backend: Django, Flask, Node.js, Express")
        p.drawString(100, 480, "• Databases: PostgreSQL, MongoDB, Redis")
        p.drawString(100, 460, "• Cloud: AWS, Docker, Kubernetes, Terraform")
        p.drawString(100, 440, "")
        
        p.drawString(100, 410, "EXPERIENCE")
        p.drawString(100, 390, "Senior Software Engineer | TechCorp Inc. | 2019-Present")
        p.drawString(100, 370, "• Led development of microservices architecture serving 1M+ users")
        p.drawString(100, 350, "• Improved system performance by 40% through optimization")
        p.drawString(100, 330, "• Mentored 4 junior developers and conducted code reviews")
        p.drawString(100, 310, "• Implemented CI/CD pipelines reducing deployment time by 60%")
        p.drawString(100, 290, "")
        
        p.drawString(100, 260, "Software Engineer | StartupXYZ | 2017-2019")
        p.drawString(100, 240, "• Built full-stack web applications using React and Python")
        p.drawString(100, 220, "• Designed and implemented RESTful APIs")
        p.drawString(100, 200, "• Collaborated with product team on feature development")
        
        p.showPage()
        p.save()
        
        # Get PDF content
        pdf_content = buffer.getvalue()
        buffer.close()
        
        print("✅ Test PDF created successfully")
        
    except ImportError:
        print("⚠️  ReportLab not installed. Using simple text for testing.")
        # Fallback: create a simple text-based test
        pdf_content = None
        test_text = """
        SARAH JOHNSON
        Senior Software Engineer
        sarah.johnson@email.com | (555) 123-4567

        PROFESSIONAL SUMMARY
        Experienced software engineer with 7+ years in full-stack development.
        Expertise in Python, React, and cloud technologies. Led teams of 6+ engineers.

        TECHNICAL SKILLS
        • Programming: Python, JavaScript, TypeScript, Java, Go
        • Frontend: React, Vue.js, Angular, HTML5, CSS3
        • Backend: Django, Flask, Node.js, Express
        • Databases: PostgreSQL, MongoDB, Redis
        • Cloud: AWS, Docker, Kubernetes, Terraform

        EXPERIENCE
        Senior Software Engineer | TechCorp Inc. | 2019-Present
        • Led development of microservices architecture serving 1M+ users
        • Improved system performance by 40% through optimization
        • Mentored 4 junior developers and conducted code reviews
        • Implemented CI/CD pipelines reducing deployment time by 60%

        Software Engineer | StartupXYZ | 2017-2019
        • Built full-stack web applications using React and Python
        • Designed and implemented RESTful APIs
        • Collaborated with product team on feature development
        """
    
    # Step 2: Extract text from PDF
    print("\n📄 Step 2: Extracting text from PDF...")
    
    if pdf_content:
        extracted_text = PDFParser.extract_text_from_pdf(pdf_content)
        if extracted_text:
            print("✅ Text extraction successful!")
            print(f"📊 Extracted {len(extracted_text)} characters")
            print("\n--- Extracted Text Preview ---")
            print(extracted_text[:200] + "..." if len(extracted_text) > 200 else extracted_text)
            print("--- End Preview ---\n")
        else:
            print("❌ Text extraction failed")
            return
    else:
        extracted_text = test_text
        print("✅ Using fallback text for testing")
    
    # Step 3: Analyze with LLM
    print("🤖 Step 3: Analyzing resume with ASI:One LLM...")
    
    llm_agent = SimpleLLMAgent("test_analyzer")
    
    prompt = f"""
    Analyze the following resume and extract key information.
    
    Candidate Name: Sarah Johnson
    Resume Content:
    {extracted_text}
    
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
    
    result = await llm_agent.query_llm(prompt)
    
    if result["success"]:
        print("✅ LLM analysis successful!")
        
        # Parse the JSON response
        analysis = llm_agent.parse_json_response(result["content"])
        
        if analysis:
            print("\n🎯 ANALYSIS RESULTS:")
            print("=" * 30)
            print(f"👤 Candidate: Sarah Johnson")
            print(f"💼 Experience Level: {analysis.get('experience_level', 'Unknown')}")
            print(f"📅 Years of Experience: {analysis.get('experience_years', 'Unknown')}")
            print(f"🛠️  Technical Skills: {', '.join(analysis.get('skills', []))}")
            print(f"\n🏆 Key Achievements:")
            for achievement in analysis.get('key_achievements', []):
                print(f"   • {achievement}")
            print(f"\n📝 Analysis Summary:")
            print(f"   {analysis.get('analysis', 'No analysis provided')}")
            print("=" * 30)
            
            print("\n✅ FULL PIPELINE TEST COMPLETED SUCCESSFULLY! 🎉")
            
        else:
            print("❌ Failed to parse LLM response")
            print(f"Raw response: {result['content']}")
    else:
        print(f"❌ LLM analysis failed: {result['content']}")

if __name__ == "__main__":
    asyncio.run(test_full_pipeline()) 