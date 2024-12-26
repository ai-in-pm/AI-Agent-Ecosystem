import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from generate_test_data import (
    generate_revenue_data,
    generate_system_metrics,
    generate_agent_metrics
)

def plot_revenue_trends(revenue_data):
    """Plot revenue trends over time."""
    dates = [datetime.fromisoformat(d["date"]) for d in revenue_data]
    amounts = [d["amount"] for d in revenue_data]
    
    plt.figure(figsize=(12, 6))
    plt.plot(dates, amounts, marker='o')
    plt.title('Revenue Trends')
    plt.xlabel('Date')
    plt.ylabel('Revenue (USD)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('demonstration/plots/revenue_trends.png')
    plt.close()

def plot_system_metrics(metrics_data):
    """Plot system metrics over time."""
    timestamps = [datetime.fromisoformat(m["timestamp"]) for m in metrics_data]
    cpu_usage = [m["cpu_usage"] for m in metrics_data]
    memory_usage = [m["memory_usage"] for m in metrics_data]
    error_rate = [m["error_rate"] * 100 for m in metrics_data]  # Convert to percentage
    
    plt.figure(figsize=(15, 8))
    
    plt.subplot(3, 1, 1)
    plt.plot(timestamps, cpu_usage, color='blue', marker='o')
    plt.title('CPU Usage Over Time')
    plt.ylabel('CPU Usage (%)')
    plt.grid(True)
    
    plt.subplot(3, 1, 2)
    plt.plot(timestamps, memory_usage, color='green', marker='o')
    plt.title('Memory Usage Over Time')
    plt.ylabel('Memory Usage (%)')
    plt.grid(True)
    
    plt.subplot(3, 1, 3)
    plt.plot(timestamps, error_rate, color='red', marker='o')
    plt.title('Error Rate Over Time')
    plt.ylabel('Error Rate (%)')
    plt.xlabel('Time')
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('demonstration/plots/system_metrics.png')
    plt.close()

def plot_agent_performance(agent_metrics):
    """Plot agent performance metrics."""
    plt.figure(figsize=(15, 10))
    
    # Success Rate Comparison
    plt.subplot(2, 2, 1)
    for agent_type, metrics in agent_metrics.items():
        dates = [datetime.fromisoformat(m["date"]) for m in metrics]
        success_rates = [m["success_rate"] * 100 for m in metrics]
        plt.plot(dates, success_rates, marker='o', label=agent_type)
    plt.title('Agent Success Rates')
    plt.ylabel('Success Rate (%)')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    
    # Execution Time Comparison
    plt.subplot(2, 2, 2)
    for agent_type, metrics in agent_metrics.items():
        dates = [datetime.fromisoformat(m["date"]) for m in metrics]
        exec_times = [m["execution_time"] for m in metrics]
        plt.plot(dates, exec_times, marker='o', label=agent_type)
    plt.title('Agent Execution Times')
    plt.ylabel('Execution Time (s)')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    
    # Task Count Comparison
    plt.subplot(2, 2, 3)
    avg_task_counts = []
    agent_types = []
    for agent_type, metrics in agent_metrics.items():
        avg_task_count = sum(m["task_count"] for m in metrics) / len(metrics)
        avg_task_counts.append(avg_task_count)
        agent_types.append(agent_type)
    
    plt.bar(agent_types, avg_task_counts)
    plt.title('Average Daily Task Count by Agent')
    plt.ylabel('Average Tasks per Day')
    plt.xticks(rotation=45)
    
    # Resource Usage Distribution
    plt.subplot(2, 2, 4)
    for agent_type, metrics in agent_metrics.items():
        resource_usage = [m["resource_usage"] for m in metrics]
        sns.kdeplot(resource_usage, label=agent_type)
    plt.title('Resource Usage Distribution')
    plt.xlabel('Resource Usage (%)')
    plt.ylabel('Density')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    plt.savefig('demonstration/plots/agent_performance.png')
    plt.close()

def generate_analytics_report():
    """Generate and visualize analytics data."""
    # Create plots directory if it doesn't exist
    import os
    os.makedirs('demonstration/plots', exist_ok=True)
    
    # Generate test data
    revenue_data = generate_revenue_data(30)  # 30 days of revenue data
    system_metrics = generate_system_metrics(24)  # 24 hours of system metrics
    agent_metrics = generate_agent_metrics(5, 7)  # 5 agents, 7 days of data
    
    # Generate plots
    plot_revenue_trends(revenue_data)
    plot_system_metrics(system_metrics)
    plot_agent_performance(agent_metrics)
    
    print("Analytics visualizations have been generated in the 'demonstration/plots' directory:")
    print("1. Revenue Trends: plots/revenue_trends.png")
    print("2. System Metrics: plots/system_metrics.png")
    print("3. Agent Performance: plots/agent_performance.png")

if __name__ == "__main__":
    # Set the style for all plots
    plt.style.use('seaborn')
    sns.set_palette("husl")
    
    # Generate analytics report
    generate_analytics_report()
