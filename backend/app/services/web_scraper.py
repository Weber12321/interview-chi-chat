import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, Optional
import re

class WebScraper:
    @staticmethod
    def scrape_webpage(url: str) -> Dict[str, Any]:
        """Scrape content from a webpage"""
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return {
                "title": soup.title.string if soup.title else "",
                "content": text,
                "links": [link.get('href') for link in soup.find_all('a') if link.get('href')],
                "metadata": {
                    "url": url,
                    "status_code": response.status_code
                }
            }
        except Exception as e:
            return {
                "error": str(e),
                "url": url
            }
    
    @staticmethod
    def extract_job_description(text: str) -> Dict[str, Any]:
        """Extract structured information from job description text"""
        # Common job description patterns
        patterns = {
            "requirements": r"(?i)(requirements|qualifications|what you'll need)",
            "responsibilities": r"(?i)(responsibilities|what you'll do|key responsibilities)",
            "benefits": r"(?i)(benefits|perks|what we offer)",
            "about_company": r"(?i)(about us|company|who we are)"
        }
        
        sections = {}
        for section, pattern in patterns.items():
            matches = re.finditer(pattern, text)
            for match in matches:
                start = match.end()
                next_section = None
                for other_section, other_pattern in patterns.items():
                    if other_section != section:
                        next_match = re.search(other_pattern, text[start:])
                        if next_match:
                            if next_section is None or next_match.start() < next_section[1]:
                                next_section = (other_section, next_match.start())
                
                if next_section:
                    section_text = text[start:start + next_section[1]]
                else:
                    section_text = text[start:]
                
                sections[section] = section_text.strip()
        
        return sections 