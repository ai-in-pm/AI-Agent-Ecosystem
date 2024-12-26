import asyncio
import logging
from datetime import datetime

from src.core.agent_factory import AgentFactory
from src.core.base_agent import BaseAgent
from src.auth.auth import create_access_token, generate_api_key
from src.database.models import User, Agent, Task, AgentMetric
from src.agents.roi_optimization_agent import ROIOptimizationAgent
from src.agents.marketplace_manager_agent import MarketplaceManagerAgent
from src.agents.analytics_agent import AnalyticsAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def demonstrate_agent_ecosystem():
    """Demonstrate the functionality of the AI Agent Ecosystem."""
    logger.info("Starting Agent Ecosystem demonstration...")
    
    # Initialize agent factory
    factory = AgentFactory()
    
    # Create sample agents
    roi_agent = await factory.create_agent(
        "roi_optimization",
        "ROI_Agent_1",
        config={"target_roi": 0.15}
    )
    
    marketplace_agent = await factory.create_agent(
        "marketplace_manager",
        "Marketplace_Agent_1",
        config={"commission_rate": 0.10}
    )
    
    analytics_agent = await factory.create_agent(
        "analytics",
        "Analytics_Agent_1",
        config={"metrics_window": "24h"}
    )
    
    # Demonstrate ROI Optimization
    logger.info("\n=== ROI Optimization Demo ===")
    roi_result = await roi_agent.execute({
        "type": "optimize_roi",
        "data": {
            "current_revenue": 100000,
            "current_costs": 80000,
            "target_roi": 0.15
        }
    })
    logger.info(f"ROI Optimization result: {roi_result}")
    
    # Demonstrate Marketplace Management
    logger.info("\n=== Marketplace Management Demo ===")
    marketplace_result = await marketplace_agent.execute({
        "type": "analyze_marketplace",
        "data": {
            "active_listings": 100,
            "total_transactions": 50,
            "average_price": 199.99
        }
    })
    logger.info(f"Marketplace analysis: {marketplace_result}")
    
    # Demonstrate Analytics
    logger.info("\n=== Analytics Demo ===")
    analytics_result = await analytics_agent.execute({
        "type": "generate_report",
        "data": {
            "timeframe": "last_24h",
            "metrics": ["revenue", "user_growth", "agent_performance"]
        }
    })
    logger.info(f"Analytics report: {analytics_result}")
    
    # Monitor agent performance
    logger.info("\n=== Agent Performance Monitoring ===")
    for agent in [roi_agent, marketplace_agent, analytics_agent]:
        metrics = await agent.monitor()
        logger.info(f"{agent.name} metrics: {metrics}")
    
    # Demonstrate agent collaboration
    logger.info("\n=== Agent Collaboration Demo ===")
    # ROI agent requests marketplace data
    marketplace_data = await marketplace_agent.execute({
        "type": "get_marketplace_stats",
        "requester": "roi_optimization"
    })
    
    # Analytics agent analyzes the combined data
    collaboration_result = await analytics_agent.execute({
        "type": "analyze_data",
        "data": {
            "roi_data": roi_result,
            "marketplace_data": marketplace_data
        }
    })
    logger.info(f"Collaboration result: {collaboration_result}")
    
    logger.info("\nDemonstration completed successfully!")

if __name__ == "__main__":
    asyncio.run(demonstrate_agent_ecosystem())
