# AI Agent Ecosystem

A powerful, scalable ecosystem for managing and monitoring AI agents. This system provides a framework for deploying, managing, and monitoring multiple AI agents working together to accomplish complex tasks.

## Features

- **Multiple Agent Types**
  - ROI Optimization Agent
  - Marketplace Manager Agent
  - Analytics Agent

- **Real-time Monitoring**
  - Health checks
  - Performance metrics
  - Resource utilization
  - Error tracking

- **Modern Web Interface**
  - Real-time dashboard
  - Agent management
  - Metrics visualization
  - System configuration

## Architecture

The system consists of several components:

1. **Backend (FastAPI)**
   - RESTful API endpoints
   - Agent management
   - Metrics collection
   - Health monitoring

2. **Frontend (React)**
   - Modern Material-UI interface
   - Real-time updates
   - Interactive dashboards
   - Configuration management

3. **Monitoring Stack**
   - Prometheus for metrics collection
   - Grafana for visualization
   - Custom dashboards

## Prerequisites

- Python 3.8+
- Node.js 14+
- Docker and Docker Compose
- Git

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-agent-ecosystem.git
cd ai-agent-ecosystem
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install frontend dependencies:
```bash
cd frontend
npm install
cd ..
```

4. Start the monitoring stack:
```bash
docker compose up -d
```

5. Start the backend server:
```bash
python -m src.main
```

6. Start the frontend development server:
```bash
cd frontend
npm start
```

## Configuration

1. Backend configuration is managed through environment variables. Copy `.env.sample` to `.env` and adjust as needed.

2. Frontend configuration can be modified in `frontend/.env`.

3. Monitoring stack configuration:
   - Prometheus: `prometheus.yml`
   - Grafana: `grafana/provisioning/`

## Usage

1. Access the web interface at http://localhost:3002

2. Monitor your agents:
   - Dashboard: http://localhost:3002/
   - Agents: http://localhost:3002/agents
   - Metrics: http://localhost:3002/metrics
   - Settings: http://localhost:3002/settings

3. Access monitoring tools:
   - Prometheus: http://localhost:9090
   - Grafana: http://localhost:3003 (admin/admin)

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

1. **Adding New Agents**
   - Extend the `BaseAgent` class
   - Implement required methods
   - Register in `AgentFactory`

2. **Adding Metrics**
   - Use the `MetricsCollector` class
   - Define new metrics in `metrics.py`
   - Update Grafana dashboards

3. **Custom Dashboards**
   - Add JSON definitions in `grafana/dashboards/`
   - Update provisioning configuration

## Testing

```bash
pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- FastAPI for the backend framework
- React and Material-UI for the frontend
- Prometheus and Grafana for monitoring
- All contributors and users of this project
