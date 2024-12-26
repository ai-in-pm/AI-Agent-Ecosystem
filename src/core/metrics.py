from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from typing import Dict, Any
import time

# Define metrics
REQUEST_COUNT = Counter('ai_agent_requests_total', 'Total number of requests processed', ['agent_type'])
REQUEST_LATENCY = Histogram('ai_agent_request_duration_seconds', 'Request duration in seconds', ['agent_type'])
ACTIVE_CONNECTIONS = Gauge('ai_agent_active_connections', 'Number of active connections', ['agent_type'])
ERROR_COUNT = Counter('ai_agent_errors_total', 'Total number of errors', ['agent_type', 'error_type'])
AGENT_HEALTH = Gauge('ai_agent_health_status', 'Health status of agents', ['agent_type'])

class MetricsCollector:
    @staticmethod
    def record_request(agent_type: str):
        REQUEST_COUNT.labels(agent_type=agent_type).inc()

    @staticmethod
    def record_latency(agent_type: str, duration: float):
        REQUEST_LATENCY.labels(agent_type=agent_type).observe(duration)

    @staticmethod
    def update_connections(agent_type: str, count: int):
        ACTIVE_CONNECTIONS.labels(agent_type=agent_type).set(count)

    @staticmethod
    def record_error(agent_type: str, error_type: str):
        ERROR_COUNT.labels(agent_type=agent_type, error_type=error_type).inc()

    @staticmethod
    def update_health(agent_type: str, status: float):
        """Update health status (0-1 where 1 is healthy)"""
        AGENT_HEALTH.labels(agent_type=agent_type).set(status)

    @staticmethod
    def get_metrics() -> tuple[str, str]:
        """Return metrics in Prometheus format"""
        return generate_latest(), CONTENT_TYPE_LATEST
