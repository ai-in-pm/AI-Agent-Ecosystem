from typing import Dict, Any, Type
from .base_agent import BaseAgent
from src.database.models import Agent
from src.agents.roi_optimization_agent import ROIOptimizationAgent
from src.agents.marketplace_manager_agent import MarketplaceManagerAgent
from src.agents.analytics_agent import AnalyticsAgent
import importlib
import logging

class AgentFactory:
    """Factory class for creating specialized AI agents."""
    
    def __init__(self):
        self.registered_agents: Dict[str, Type[BaseAgent]] = {}
        self.logger = logging.getLogger("agent.factory")
        
        # Register default agent types
        self.register_agent("roi_optimization", ROIOptimizationAgent)
        self.register_agent("marketplace_manager", MarketplaceManagerAgent)
        self.register_agent("analytics", AnalyticsAgent)
    
    def register_agent(self, agent_type: str, agent_class: Type[BaseAgent]) -> None:
        """Register a new agent type."""
        self.registered_agents[agent_type] = agent_class
        self.logger.info(f"Registered new agent type: {agent_type}")
    
    async def create_agent(self, agent_type: str, name: str, config: Dict[str, Any]) -> BaseAgent:
        """Create a new agent instance."""
        if agent_type not in self.registered_agents:
            raise ValueError(f"Unknown agent type: {agent_type}")
            
        agent_class = self.registered_agents[agent_type]
        agent = agent_class(name=name, config=config)
        
        # Initialize the agent
        success = await agent.initialize()
        if not success:
            raise RuntimeError(f"Failed to initialize agent: {name}")
            
        self.logger.info(f"Created new agent: {name} of type {agent_type}")
        return agent
    
    def get_available_agent_types(self) -> list[str]:
        """Get list of all registered agent types."""
        return list(self.registered_agents.keys())
    
    async def create_specialized_agent(self, 
                                     agent_type: str,
                                     name: str,
                                     config: Dict[str, Any],
                                     specialization: Dict[str, Any]) -> BaseAgent:
        """Create a specialized agent with custom parameters."""
        base_agent = await self.create_agent(agent_type, name, config)
        
        # Apply specialization
        for key, value in specialization.items():
            if hasattr(base_agent, key):
                setattr(base_agent, key, value)
                
        self.logger.info(f"Created specialized agent: {name} with {len(specialization)} custom parameters")
        return base_agent
