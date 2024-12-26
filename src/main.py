import asyncio
import logging
import time
from typing import Dict, Any
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from src.core.agent_factory import AgentFactory
from src.core.metrics import MetricsCollector
from src.agents import (
    ROIOptimizationAgent,
    MarketplaceManagerAgent,
    AnalyticsAgent
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="AI Agent Ecosystem")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agent factory
agent_factory = AgentFactory()

async def initialize_ecosystem() -> Dict[str, Any]:
    """Initialize all core agents in the ecosystem."""
    agents = {}
    
    # Register all agent types
    agent_classes = {
        "roi_optimization": ROIOptimizationAgent,
        "marketplace_manager": MarketplaceManagerAgent,
        "analytics": AnalyticsAgent
    }
    
    for agent_type, agent_class in agent_classes.items():
        agent_factory.register_agent(agent_type, agent_class)
        
        # Create an instance of each agent type
        try:
            agent = await agent_factory.create_agent(
                agent_type,
                f"{agent_type}_agent",
                config={}
            )
            agents[agent_type] = agent
            logger.info(f"Successfully initialized {agent_type} agent")
            
            # Record metrics for successful initialization
            MetricsCollector.update_health(agent_type, 1.0)
            MetricsCollector.update_connections(agent_type, 1)
        except Exception as e:
            logger.error(f"Failed to initialize {agent_type} agent: {str(e)}")
            MetricsCollector.record_error(agent_type, "initialization_error")
            MetricsCollector.update_health(agent_type, 0.0)
    
    return agents

@app.on_event("startup")
async def startup_event():
    """Initialize the ecosystem on startup."""
    logger.info("Initializing AI Agent Ecosystem...")
    await initialize_ecosystem()
    logger.info("AI Agent Ecosystem initialized successfully")

@app.get("/health")
async def health_check():
    """Check the health of all agents."""
    start_time = time.time()
    agents = await initialize_ecosystem()
    health_status = {}
    
    for agent_type, agent in agents.items():
        try:
            status = await agent.monitor()
            health_status[agent_type] = status
            MetricsCollector.record_request(agent_type)
        except Exception as e:
            logger.error(f"Health check failed for {agent_type}: {str(e)}")
            MetricsCollector.record_error(agent_type, "health_check_error")
    
    duration = time.time() - start_time
    for agent_type in agents:
        MetricsCollector.record_latency(agent_type, duration)
    
    return health_status

@app.get("/metrics")
async def get_metrics():
    """Get metrics from all agents."""
    agents = await initialize_ecosystem()
    metrics = {}
    
    for agent_type, agent in agents.items():
        try:
            metrics[agent_type] = await agent.report_metrics()
            MetricsCollector.record_request(agent_type)
        except Exception as e:
            logger.error(f"Failed to get metrics for {agent_type}: {str(e)}")
            MetricsCollector.record_error(agent_type, "metrics_error")
    
    return metrics

@app.get("/prometheus-metrics")
async def prometheus_metrics():
    """Expose metrics in Prometheus format."""
    metrics_data, content_type = MetricsCollector.get_metrics()
    return Response(content=metrics_data, media_type=content_type)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
