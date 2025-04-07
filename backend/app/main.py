from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, Field
from typing import Optional, List
import uvicorn
from .agents.hr_agent import HRAgent
from .agents.interviewer_agent import InterviewerAgent
from .agents.supervisor_agent import SupervisorAgent
from .core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A multi-agent workflow system for conducting technical interviews using OpenAI's agent framework.",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents
hr_agent = HRAgent()
interviewer_agent = InterviewerAgent()
supervisor_agent = SupervisorAgent()

class InterviewRequest(BaseModel):
    """Request model for starting an interview"""
    cv_url: Optional[str] = Field(None, description="URL to the candidate's CV")
    job_description_url: str = Field(..., description="URL to the job description")
    company_website_url: str = Field(..., description="URL to the company website")
    cv_text: Optional[str] = Field(None, description="Raw CV text content")

    class Config:
        schema_extra = {
            "example": {
                "cv_url": "https://example.com/cv.pdf",
                "job_description_url": "https://example.com/job",
                "company_website_url": "https://example.com",
                "cv_text": "Optional raw CV text"
            }
        }

class AgentResponse(BaseModel):
    """Response model for agent interactions"""
    agent: str = Field(..., description="Name of the agent")
    response: str = Field(..., description="Agent's response text")
    data: Optional[dict] = Field(None, description="Additional data from the agent")

    class Config:
        schema_extra = {
            "example": {
                "agent": "HR Agent",
                "response": "I have analyzed the CV and created an interview agenda.",
                "data": {
                    "agenda": {
                        "technical_interview": {
                            "topics": ["Python", "System Design"],
                            "duration": "60 minutes"
                        }
                    }
                }
            }
        }

@app.post(
    "/api/v1/start-interview",
    response_model=List[AgentResponse],
    summary="Start a new interview process",
    description="Initiates the interview process with all three agents (HR, Interviewer, and Supervisor).",
    response_description="List of responses from all agents in the workflow."
)
async def start_interview(request: InterviewRequest):
    """
    Start a new interview process with the following steps:
    1. HR Agent analyzes CV and job description
    2. Interviewer Agent conducts the interview
    3. Supervisor Agent evaluates the interview
    
    Args:
        request (InterviewRequest): Contains CV and job information
        
    Returns:
        List[AgentResponse]: Responses from all agents in the workflow
    """
    try:
        # HR Agent processes CV and job description
        hr_response = await hr_agent.process_input({
            "cv_url": request.cv_url,
            "job_description_url": request.job_description_url,
            "company_website_url": request.company_website_url,
            "cv_text": request.cv_text
        })
        
        # Interviewer Agent conducts the interview
        interviewer_response = await interviewer_agent.process_input({
            "agenda": hr_response["data"]["agenda"],
            "candidate_info": hr_response["data"]["candidate_info"]
        })
        
        # Supervisor Agent evaluates the interview
        supervisor_response = await supervisor_agent.process_input({
            "interview_data": interviewer_response["data"],
            "job_requirements": hr_response["data"]["job_requirements"]
        })
        
        return [
            AgentResponse(agent="HR Agent", response=hr_response["response"], data=hr_response["data"]),
            AgentResponse(agent="Interviewer Agent", response=interviewer_response["response"], data=interviewer_response["data"]),
            AgentResponse(agent="Supervisor Agent", response=supervisor_response["response"], data=supervisor_response["data"])
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post(
    "/api/v1/upload-cv",
    summary="Upload a CV file",
    description="Upload a CV file in PDF format for processing.",
    response_description="Confirmation of file upload"
)
async def upload_cv(file: UploadFile = File(..., description="PDF file containing the candidate's CV")):
    """
    Upload a CV file for processing.
    
    Args:
        file (UploadFile): PDF file containing the candidate's CV
        
    Returns:
        dict: Confirmation of file upload with filename
    """
    try:
        # Handle CV file upload
        # Implementation for file processing
        return {"filename": file.filename, "status": "uploaded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Add custom documentation
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 