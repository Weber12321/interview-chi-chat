from typing import Dict, Any, List
from langchain.agents import AgentExecutor
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from ..core.config import settings

class BaseAgent:
    def __init__(self, name: str, tools: List[Any] = None):
        self.name = name
        self.tools = tools or []
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        
        self.llm = ChatOpenAI(
            model_name=settings.OPENAI_MODEL,
            temperature=0.7,
            openai_api_key=settings.OPENAI_API_KEY,
            openai_api_base=settings.OPENAI_API_BASE
        )
        
        self.agent_executor = None
    
    def initialize_agent(self):
        """Initialize the agent with its specific configuration"""
        raise NotImplementedError
    
    async def process_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data and return agent's response"""
        if not self.agent_executor:
            self.initialize_agent()
        
        response = await self.agent_executor.arun(input_data)
        return {"response": response}
    
    def get_memory(self) -> Dict[str, Any]:
        """Get the current state of the agent's memory"""
        return self.memory.load_memory_variables({})
    
    def clear_memory(self):
        """Clear the agent's memory"""
        self.memory.clear() 