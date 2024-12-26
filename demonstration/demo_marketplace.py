import asyncio
import logging
from datetime import datetime
from src.agents.marketplace_manager_agent import MarketplaceManagerAgent
from generate_test_data import generate_marketplace_listings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def demonstrate_marketplace():
    """Demonstrate marketplace functionality."""
    logger.info("Starting Marketplace demonstration...")
    
    # Initialize marketplace agent
    marketplace_agent = MarketplaceManagerAgent(
        name="marketplace_demo",
        config={"commission_rate": 0.15}
    )
    await marketplace_agent.initialize()
    
    # Generate sample listings
    sample_listings = generate_marketplace_listings(10)
    
    # Create listings
    logger.info("\n=== Creating Sample Listings ===")
    for listing in sample_listings:
        result = await marketplace_agent.execute({
            "type": "create_listing",
            "seller_id": listing["seller_id"],
            "listing_data": listing
        })
        logger.info(f"Created listing: {listing['name']} (ID: {result.get('listing_id')})")
    
    # Simulate purchases
    logger.info("\n=== Simulating Purchases ===")
    for i in range(3):
        listing_id = f"listing_{i+1}"
        result = await marketplace_agent.execute({
            "type": "process_purchase",
            "buyer_id": f"buyer_{1000 + i}",
            "listing_id": listing_id
        })
        logger.info(f"Purchase processed: {result}")
    
    # Get marketplace metrics
    logger.info("\n=== Marketplace Metrics ===")
    metrics = await marketplace_agent.monitor()
    logger.info("Current marketplace status:")
    logger.info(f"Active listings: {metrics['metrics']['listings']['active']}")
    logger.info(f"Total transactions: {metrics['metrics']['transactions']['total']}")
    logger.info(f"Revenue metrics: {metrics['metrics']['revenue']}")
    
    # Check marketplace health
    logger.info("\n=== Marketplace Health ===")
    health = metrics["health"]
    logger.info(f"Overall health: {health['overall']}")
    logger.info("Health checks:")
    for component, status in health["checks"].items():
        logger.info(f"- {component}: {status}")
    
    # Demonstrate search and filtering
    logger.info("\n=== Search and Filtering ===")
    analytics_listings = [
        listing for listing in marketplace_agent.listings.values()
        if listing["category"] == "analytics"
    ]
    logger.info(f"Found {len(analytics_listings)} analytics listings")
    
    high_value_listings = [
        listing for listing in marketplace_agent.listings.values()
        if listing["price"] > 200
    ]
    logger.info(f"Found {len(high_value_listings)} high-value listings (>$200)")
    
    # Demonstrate listing updates
    logger.info("\n=== Updating Listings ===")
    if marketplace_agent.listings:
        first_listing_id = next(iter(marketplace_agent.listings))
        update_result = await marketplace_agent.execute({
            "type": "update_listing",
            "listing_id": first_listing_id,
            "updates": {
                "price": 149.99,
                "description": "Updated description with special offer!"
            }
        })
        logger.info(f"Updated listing: {update_result}")
    
    # Print marketplace summary
    logger.info("\n=== Marketplace Summary ===")
    categories = {}
    total_value = 0
    
    for listing in marketplace_agent.listings.values():
        category = listing["category"]
        categories[category] = categories.get(category, 0) + 1
        if listing["status"] == "active":
            total_value += listing["price"]
    
    logger.info("Listings by category:")
    for category, count in categories.items():
        logger.info(f"- {category}: {count} listings")
    
    logger.info(f"\nTotal marketplace value: ${total_value:,.2f}")
    
    logger.info("\nDemonstration completed successfully!")

if __name__ == "__main__":
    asyncio.run(demonstrate_marketplace())
