from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime
import logging
import asyncio
from src.database.models import AgentMetric

class BaseAgent(ABC):
    """Base class for all AI agents in the ecosystem."""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.created_at = datetime.utcnow()
        self.last_active = datetime.utcnow()
        self.status = "initialized"
        self.logger = logging.getLogger(f"agent.{name}")
        self.metrics = []
    
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize the agent with necessary setup."""
        pass
    
    @abstractmethod
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the main task of the agent."""
        pass
    
    @abstractmethod
    async def monitor(self) -> Dict[str, Any]:
        """Monitor agent's performance and health."""
        metrics = {
            "name": self.name,
            "status": self.status,
            "last_active": self.last_active.isoformat(),
            "uptime": (datetime.utcnow() - self.created_at).total_seconds(),
            "metrics": {}
        }
        return metrics
    
    async def record_metric(self, name: str, value: Any) -> None:
        """Record a metric for monitoring."""
        metric = {
            "name": name,
            "value": value,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.metrics.append(metric)
        self.logger.debug(f"Recorded metric: {name}={value}")
    
    async def report_metrics(self) -> Dict[str, Any]:
        """Report agent's metrics for monitoring."""
        return {
            "name": self.name,
            "status": self.status,
            "last_active": self.last_active,
            "uptime": (datetime.utcnow() - self.created_at).total_seconds(),
            "metrics": self.metrics
        }
    
    async def collaborate(self, target_agent: 'BaseAgent', message: Dict[str, Any]) -> Dict[str, Any]:
        """Collaborate with another agent."""
        self.logger.info(f"Collaborating with {target_agent.name}")
        return await target_agent.receive_message(self, message)
    
    async def receive_message(self, sender: 'BaseAgent', message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming messages from other agents."""
        self.logger.info(f"Received message from {sender.name}")
        return {"status": "received", "from": sender.name, "timestamp": datetime.utcnow()}
    
    async def optimize(self) -> Dict[str, Any]:
        """Optimize agent's performance based on metrics."""
        self.logger.info("Running optimization routine")
        return await self.monitor()
    
    def __str__(self) -> str:
        return f"{self.name} Agent (Status: {self.status})"
