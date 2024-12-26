import pytest
from datetime import datetime
from src.core.base_agent import BaseAgent

class TestAgent(BaseAgent):
    """Test implementation of BaseAgent."""
    
    async def initialize(self) -> bool:
        return True
        
    async def execute(self, task: dict) -> dict:
        return {"status": "success", "task": task}
        
    async def monitor(self) -> dict:
        return {"status": "healthy"}

@pytest.fixture
def agent():
    """Create test agent instance."""
    return TestAgent(name="test_agent", config={"test": True})

@pytest.mark.asyncio
async def test_agent_initialization(agent):
    """Test agent initialization."""
    assert agent.name == "test_agent"
    assert agent.config == {"test": True}
    assert agent.status == "initialized"
    
@pytest.mark.asyncio
async def test_agent_execution(agent):
    """Test agent task execution."""
    task = {"type": "test_task"}
    result = await agent.execute(task)
    assert result["status"] == "success"
    assert result["task"] == task
    
@pytest.mark.asyncio
async def test_agent_monitoring(agent):
    """Test agent monitoring."""
    result = await agent.monitor()
    assert result["status"] == "healthy"
    
@pytest.mark.asyncio
async def test_agent_metrics(agent):
    """Test agent metrics reporting."""
    metrics = await agent.report_metrics()
    assert metrics["name"] == "test_agent"
    assert metrics["status"] == "initialized"
    assert "last_active" in metrics
    assert "uptime" in metrics
    
@pytest.mark.asyncio
async def test_agent_collaboration(agent):
    """Test agent collaboration."""
    other_agent = TestAgent(name="other_agent", config={"test": True})
    message = {"type": "test_message"}
    
    result = await agent.collaborate(other_agent, message)
    assert result["status"] == "received"
    assert result["from"] == "test_agent"
    
@pytest.mark.asyncio
async def test_agent_message_receiving(agent):
    """Test agent message receiving."""
    other_agent = TestAgent(name="sender", config={"test": True})
    message = {"type": "test_message"}
    
    result = await agent.receive_message(other_agent, message)
    assert result["status"] == "received"
    assert result["from"] == "sender"
    
@pytest.mark.asyncio
async def test_agent_optimization(agent):
    """Test agent optimization."""
    result = await agent.optimize()
    assert result["status"] == "healthy"
    
@pytest.mark.asyncio
async def test_agent_string_representation(agent):
    """Test agent string representation."""
    assert str(agent) == "test_agent Agent (Status: initialized)"
    
@pytest.mark.asyncio
async def test_agent_status_update(agent):
    """Test agent status updates."""
    original_status = agent.status
    agent.status = "running"
    assert agent.status == "running"
    assert agent.status != original_status
    
@pytest.mark.asyncio
async def test_agent_last_active_update(agent):
    """Test agent last active timestamp updates."""
    original_timestamp = agent.last_active
    await agent.execute({"type": "test_task"})
    assert agent.last_active > original_timestamp
