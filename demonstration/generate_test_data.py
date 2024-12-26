import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

def generate_revenue_data(days: int = 30) -> List[Dict[str, Any]]:
    """Generate sample revenue data."""
    base_revenue = 1000
    data = []
    
    for i in range(days):
        date = datetime.now() - timedelta(days=i)
        daily_revenue = base_revenue + random.uniform(-200, 500)
        data.append({
            "date": date.isoformat(),
            "amount": round(daily_revenue, 2),
            "source": random.choice(["subscription", "marketplace", "services"]),
            "currency": "USD"
        })
    
    return data

def generate_marketplace_listings(count: int = 10) -> List[Dict[str, Any]]:
    """Generate sample marketplace listings."""
    categories = ["analytics", "automation", "integration", "productivity", "custom"]
    listings = []
    
    for i in range(count):
        price = random.uniform(9.99, 499.99)
        listings.append({
            "name": f"AI Agent Package {i+1}",
            "description": f"Advanced AI agent solution for {random.choice(categories)}",
            "price": round(price, 2),
            "category": random.choice(categories),
            "seller_id": f"seller_{random.randint(1000, 9999)}",
            "status": random.choice(["active", "pending", "inactive"]),
            "rating": round(random.uniform(3.5, 5.0), 1)
        })
    
    return listings

def generate_system_metrics(hours: int = 24) -> List[Dict[str, Any]]:
    """Generate sample system metrics."""
    metrics = []
    
    for i in range(hours):
        timestamp = datetime.now() - timedelta(hours=i)
        metrics.append({
            "timestamp": timestamp.isoformat(),
            "cpu_usage": round(random.uniform(20, 80), 1),
            "memory_usage": round(random.uniform(30, 85), 1),
            "error_rate": round(random.uniform(0, 0.02), 3),
            "response_time": round(random.uniform(50, 200), 2)
        })
    
    return metrics

def generate_agent_metrics(agent_count: int = 5, days: int = 7) -> Dict[str, List[Dict[str, Any]]]:
    """Generate sample agent performance metrics."""
    agent_types = ["roi_optimization", "marketplace_manager", "analytics", 
                  "content_creator", "community_engagement"]
    metrics = {}
    
    for i in range(agent_count):
        agent_type = agent_types[i]
        agent_metrics = []
        
        for j in range(days):
            date = datetime.now() - timedelta(days=j)
            agent_metrics.append({
                "date": date.isoformat(),
                "execution_time": round(random.uniform(0.1, 2.0), 2),
                "success_rate": round(random.uniform(0.85, 0.99), 2),
                "task_count": random.randint(100, 1000),
                "resource_usage": round(random.uniform(10, 60), 1)
            })
        
        metrics[agent_type] = agent_metrics
    
    return metrics

def generate_user_data(count: int = 5) -> List[Dict[str, Any]]:
    """Generate sample user data."""
    roles = ["admin", "user", "developer"]
    users = []
    
    for i in range(count):
        users.append({
            "id": f"user_{random.randint(1000, 9999)}",
            "email": f"user{i+1}@example.com",
            "role": random.choice(roles),
            "is_active": random.choice([True, True, True, False]),  # 75% active
            "created_at": (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat()
        })
    
    return users

def generate_task_data(count: int = 20) -> List[Dict[str, Any]]:
    """Generate sample task data."""
    task_types = ["analysis", "optimization", "monitoring", "reporting"]
    statuses = ["pending", "running", "completed", "failed"]
    tasks = []
    
    for i in range(count):
        created_at = datetime.now() - timedelta(hours=random.randint(1, 48))
        status = random.choice(statuses)
        
        task = {
            "id": f"task_{random.randint(1000, 9999)}",
            "type": random.choice(task_types),
            "agent_id": f"agent_{random.randint(1000, 9999)}",
            "status": status,
            "created_at": created_at.isoformat(),
            "data": {
                "parameter1": random.randint(1, 100),
                "parameter2": f"value_{random.randint(1, 10)}"
            }
        }
        
        if status in ["completed", "failed"]:
            completed_at = created_at + timedelta(minutes=random.randint(5, 60))
            task["completed_at"] = completed_at.isoformat()
            
            if status == "completed":
                task["result"] = {
                    "success": True,
                    "output": f"Sample output for task {i+1}"
                }
            else:
                task["result"] = {
                    "success": False,
                    "error": "Sample error message"
                }
        
        tasks.append(task)
    
    return tasks

if __name__ == "__main__":
    # Generate all test data
    test_data = {
        "revenue": generate_revenue_data(),
        "marketplace_listings": generate_marketplace_listings(),
        "system_metrics": generate_system_metrics(),
        "agent_metrics": generate_agent_metrics(),
        "users": generate_user_data(),
        "tasks": generate_task_data()
    }
    
    # Print sample data
    print("\n=== Sample Test Data ===")
    for category, data in test_data.items():
        print(f"\n{category.upper()}:")
        if isinstance(data, dict):
            print(f"Generated {len(data)} agent metrics sets")
            print("Sample:", list(data.values())[0][0])
        else:
            print(f"Generated {len(data)} records")
            print("Sample:", data[0])
