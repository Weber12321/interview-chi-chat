from typing import Dict, Any, List
from langchain.agents import Tool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from .base_agent import BaseAgent

class HRAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="HR Agent")
        self.tools = [
            Tool(
                name="parse_cv",
                func=self._parse_cv,
                description="Parse a CV document and extract relevant information"
            ),
            Tool(
                name="parse_job_description",
                func=self._parse_job_description,
                description="Parse a job description and extract requirements"
            ),
            Tool(
                name="create_interview_agenda",
                func=self._create_interview_agenda,
                description="Create an interview agenda based on CV and job description"
            )
        ]
    
    def initialize_agent(self):
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an HR agent specialized in technical hiring. Your role is to:
            1. Analyze candidate CVs and job descriptions
            2. Create comprehensive interview agendas
            3. Identify key technical areas to assess
            4. Consider both technical and soft skills requirements"""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        agent = {
            "input": lambda x: x["input"],
            "chat_history": lambda x: x["chat_history"],
            "agent_scratchpad": lambda x: format_to_openai_function_messages(x["intermediate_steps"])
        } | prompt | self.llm | OpenAIFunctionsAgentOutputParser()
        
        self.agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)
    
    def _parse_cv(self, cv_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse CV data and extract relevant information"""
        # Implementation for CV parsing
        return {
            "skills": [],
            "experience": [],
            "education": [],
            "projects": []
        }
    
    def _parse_job_description(self, jd_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse job description and extract requirements"""
        # Implementation for job description parsing
        return {
            "required_skills": [],
            "preferred_skills": [],
            "responsibilities": [],
            "qualifications": []
        }
    
    def _create_interview_agenda(self, cv_info: Dict[str, Any], jd_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create interview agenda based on CV and job description"""
        # Implementation for agenda creation
        return {
            "technical_interview": {
                "topics": [],
                "duration": "60 minutes"
            },
            "system_design": {
                "topics": [],
                "duration": "45 minutes"
            },
            "behavioral": {
                "topics": [],
                "duration": "30 minutes"
            }
        } 