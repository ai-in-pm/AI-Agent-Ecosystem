import asyncio
import logging
import os
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def run_all_demonstrations():
    """Run all demonstration scripts."""
    start_time = datetime.now()
    logger.info("Starting AI Agent Ecosystem demonstrations...")
    
    # Create demonstration output directory
    os.makedirs('demonstration/output', exist_ok=True)
    os.makedirs('demonstration/plots', exist_ok=True)
    
    try:
        # Generate test data
        logger.info("\n=== Generating Test Data ===")
        from generate_test_data import (
            generate_revenue_data,
            generate_marketplace_listings,
            generate_system_metrics,
            generate_agent_metrics,
            generate_user_data,
            generate_task_data
        )
        
        test_data = {
            "revenue": generate_revenue_data(),
            "marketplace_listings": generate_marketplace_listings(),
            "system_metrics": generate_system_metrics(),
            "agent_metrics": generate_agent_metrics(),
            "users": generate_user_data(),
            "tasks": generate_task_data()
        }
        
        # Run ecosystem demonstration
        logger.info("\n=== Running Ecosystem Demonstration ===")
        from demo_ecosystem import demonstrate_agent_ecosystem
        await demonstrate_agent_ecosystem()
        
        # Run marketplace demonstration
        logger.info("\n=== Running Marketplace Demonstration ===")
        from demo_marketplace import demonstrate_marketplace
        await demonstrate_marketplace()
        
        # Generate analytics visualizations
        logger.info("\n=== Generating Analytics Visualizations ===")
        from visualize_analytics import generate_analytics_report
        generate_analytics_report()
        
        # Calculate execution time
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        
        # Print summary
        logger.info("\n=== Demonstration Summary ===")
        logger.info(f"Total execution time: {execution_time:.2f} seconds")
        logger.info("\nGenerated files:")
        logger.info("1. Test data")
        for category, data in test_data.items():
            if isinstance(data, dict):
                logger.info(f"   - {category}: {len(data)} sets of metrics")
            else:
                logger.info(f"   - {category}: {len(data)} records")
        
        logger.info("\n2. Analytics visualizations:")
        logger.info("   - Revenue Trends: plots/revenue_trends.png")
        logger.info("   - System Metrics: plots/system_metrics.png")
        logger.info("   - Agent Performance: plots/agent_performance.png")
        
        logger.info("\nAll demonstrations completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during demonstration: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    asyncio.run(run_all_demonstrations())
