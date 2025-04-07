from sqlalchemy import Column, String, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class Candidate(BaseModel):
    __tablename__ = "candidates"
    
    name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    cv_path = Column(String(255))
    linkedin_url = Column(String(255))
    github_url = Column(String(255))
    personal_website = Column(String(255))
    raw_cv_text = Column(Text)
    parsed_cv_data = Column(JSON)
    
    interviews = relationship("Interview", back_populates="candidate")

class JobDescription(BaseModel):
    __tablename__ = "job_descriptions"
    
    title = Column(String(255))
    company_name = Column(String(100))
    company_website = Column(String(255))
    raw_description = Column(Text)
    parsed_description = Column(JSON)
    
    interviews = relationship("Interview", back_populates="job_description")

class Interview(BaseModel):
    __tablename__ = "interviews"
    
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    job_description_id = Column(Integer, ForeignKey("job_descriptions.id"))
    agenda = Column(JSON)
    questions = Column(JSON)
    responses = Column(JSON)
    feedback = Column(JSON)
    status = Column(String(50))  # planned, in_progress, completed
    
    candidate = relationship("Candidate", back_populates="interviews")
    job_description = relationship("JobDescription", back_populates="interviews") 