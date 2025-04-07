from PyPDF2 import PdfReader
from typing import Dict, Any
import re

class PDFParser:
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        """Extract text content from a PDF file"""
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

    @staticmethod
    def parse_cv_content(text: str) -> Dict[str, Any]:
        """Parse CV content and extract structured information"""
        # Extract contact information
        email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
        phone_pattern = r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        linkedin_pattern = r'linkedin\.com/in/[a-zA-Z0-9-]+'
        github_pattern = r'github\.com/[a-zA-Z0-9-]+'
        
        emails = re.findall(email_pattern, text)
        phones = re.findall(phone_pattern, text)
        linkedin = re.findall(linkedin_pattern, text)
        github = re.findall(github_pattern, text)
        
        # Extract sections using common CV section headers
        sections = {
            "education": [],
            "experience": [],
            "skills": [],
            "projects": []
        }
        
        # Simple section detection
        section_patterns = {
            "education": r"(?i)(education|academic background|qualifications)",
            "experience": r"(?i)(experience|work history|employment)",
            "skills": r"(?i)(skills|technical skills|competencies)",
            "projects": r"(?i)(projects|portfolio|work samples)"
        }
        
        for section, pattern in section_patterns.items():
            matches = re.finditer(pattern, text)
            for match in matches:
                start = match.end()
                next_section = None
                for other_section, other_pattern in section_patterns.items():
                    if other_section != section:
                        next_match = re.search(other_pattern, text[start:])
                        if next_match:
                            if next_section is None or next_match.start() < next_section[1]:
                                next_section = (other_section, next_match.start())
                
                if next_section:
                    section_text = text[start:start + next_section[1]]
                else:
                    section_text = text[start:]
                
                sections[section].append(section_text.strip())
        
        return {
            "contact_info": {
                "emails": emails,
                "phones": phones,
                "linkedin": linkedin,
                "github": github
            },
            "sections": sections
        } 