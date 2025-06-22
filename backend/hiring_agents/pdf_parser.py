"""
PDF Parser Utility
==================

Utility for extracting text from PDF files for resume processing.
"""

import PyPDF2
import io
from typing import Optional


class PDFParser:
    """Utility class for parsing PDF files and extracting text content."""
    
    @staticmethod
    def extract_text_from_pdf(pdf_content: bytes) -> Optional[str]:
        """
        Extract text content from PDF bytes.
        
        Args:
            pdf_content: Raw PDF file content as bytes
            
        Returns:
            Extracted text as string, or None if extraction fails
        """
        try:
            # Create a file-like object from bytes
            pdf_file = io.BytesIO(pdf_content)
            
            # Create PDF reader object
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Extract text from all pages
            text_content = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text_content += page.extract_text() + "\n"
            
            # Clean up the text
            text_content = text_content.strip()
            
            if not text_content:
                return None
                
            return text_content
            
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return None
    
    @staticmethod
    def extract_text_from_file_path(file_path: str) -> Optional[str]:
        """
        Extract text content from PDF file path.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Extracted text as string, or None if extraction fails
        """
        try:
            with open(file_path, 'rb') as file:
                pdf_content = file.read()
                return PDFParser.extract_text_from_pdf(pdf_content)
        except Exception as e:
            print(f"Error reading PDF file {file_path}: {e}")
            return None 