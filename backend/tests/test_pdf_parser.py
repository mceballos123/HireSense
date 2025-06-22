#!/usr/bin/env python3
"""
Test PDF Parser
===============

Simple test script to verify PDF parsing functionality.
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from hiring_agents.pdf_parser import PDFParser

def test_pdf_parser():
    """Test the PDF parser with a sample PDF if available."""
    print("🧪 Testing PDF Parser...")
    
    # Test with a simple PDF creation
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        import io
        
        # Create a simple test PDF in memory
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        
        # Add some test content
        p.drawString(100, 750, "JOHN DOE")
        p.drawString(100, 720, "Software Engineer")
        p.drawString(100, 690, "")
        p.drawString(100, 660, "EXPERIENCE:")
        p.drawString(100, 630, "• 5 years of Python development")
        p.drawString(100, 600, "• React and JavaScript expertise")
        p.drawString(100, 570, "• Led development team of 4 engineers")
        p.drawString(100, 540, "")
        p.drawString(100, 510, "SKILLS:")
        p.drawString(100, 480, "Python, JavaScript, React, Node.js, PostgreSQL")
        
        p.showPage()
        p.save()
        
        # Get PDF content
        pdf_content = buffer.getvalue()
        buffer.close()
        
        # Test extraction
        extracted_text = PDFParser.extract_text_from_pdf(pdf_content)
        
        if extracted_text:
            print("✅ PDF parsing successful!")
            print("📄 Extracted text:")
            print("-" * 40)
            print(extracted_text)
            print("-" * 40)
        else:
            print("❌ PDF parsing failed - no text extracted")
            
    except ImportError:
        print("⚠️  ReportLab not installed, skipping PDF creation test")
        print("📋 To test with actual PDFs, install reportlab: pip install reportlab")
        print("✅ PDF parser module imported successfully")
        
    except Exception as e:
        print(f"❌ Error during PDF test: {e}")

if __name__ == "__main__":
    test_pdf_parser() 