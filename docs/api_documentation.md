# AI Agent Ecosystem API Documentation

## Overview

The AI Agent Ecosystem provides a comprehensive API for managing and interacting with various AI agents. This documentation covers all available endpoints, authentication methods, and usage examples.

## Authentication

The API uses two authentication methods:
1. JWT Bearer tokens for user authentication
2. API keys for programmatic access

### JWT Authentication

To obtain a JWT token:

```http
POST /auth/token
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "your_password"
}
```

Response:
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer"
}
```

### API Key Authentication

To generate an API key:

```http
POST /auth/api-key
Authorization: Bearer your_jwt_token
```

Response:
```json
{
    "api_key": "your_api_key_here",
    "expires_at": "2024-12-25T20:35:51Z"
}
```

## Endpoints

### Agents

#### List All Agents

```http
GET /agents
Authorization: Bearer your_jwt_token
```

Response:
```json
{
    "agents": [
        {
            "id": "agent_id",
            "name": "Agent Name",
            "type": "agent_type",
            "status": "active",
            "created_at": "2024-12-25T20:35:51Z"
        }
    ]
}
```

#### Create Agent

```http
POST /agents
Authorization: Bearer your_jwt_token
Content-Type: application/json

{
    "name": "New Agent",
    "type": "agent_type",
    "config": {
        "setting1": "value1",
        "setting2": "value2"
    }
}
```

#### Get Agent Details

```http
GET /agents/{agent_id}
Authorization: Bearer your_jwt_token
```

#### Update Agent

```http
PUT /agents/{agent_id}
Authorization: Bearer your_jwt_token
Content-Type: application/json

{
    "name": "Updated Name",
    "config": {
        "setting1": "new_value"
    }
}
```

#### Delete Agent

```http
DELETE /agents/{agent_id}
Authorization: Bearer your_jwt_token
```

### Tasks

#### Create Task

```http
POST /tasks
Authorization: Bearer your_jwt_token
Content-Type: application/json

{
    "agent_id": "agent_id",
    "type": "task_type",
    "data": {
        "param1": "value1",
        "param2": "value2"
    }
}
```

#### Get Task Status

```http
GET /tasks/{task_id}
Authorization: Bearer your_jwt_token
```

Response:
```json
{
    "id": "task_id",
    "agent_id": "agent_id",
    "type": "task_type",
    "status": "completed",
    "result": {
        "output": "task_output"
    },
    "created_at": "2024-12-25T20:35:51Z",
    "completed_at": "2024-12-25T20:36:51Z"
}
```

### Marketplace

#### List Items

```http
GET /marketplace
Authorization: Bearer your_jwt_token
```

#### Create Listing

```http
POST /marketplace
Authorization: Bearer your_jwt_token
Content-Type: application/json

{
    "name": "Item Name",
    "description": "Item Description",
    "price": 99.99,
    "category": "category_name"
}
```

#### Purchase Item

```http
POST /marketplace/{item_id}/purchase
Authorization: Bearer your_jwt_token
```

### Analytics

#### Get System Metrics

```http
GET /analytics/system
Authorization: Bearer your_jwt_token
```

#### Get Business Metrics

```http
GET /analytics/business
Authorization: Bearer your_jwt_token
```

#### Get Agent Metrics

```http
GET /analytics/agents/{agent_id}
Authorization: Bearer your_jwt_token
```

## Error Handling

The API uses standard HTTP status codes and returns error messages in the following format:

```json
{
    "error": {
        "code": "error_code",
        "message": "Error description"
    }
}
```

Common error codes:
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 429: Too Many Requests
- 500: Internal Server Error

## Rate Limiting

The API implements rate limiting based on the following rules:
- JWT Authentication: 1000 requests per hour
- API Key Authentication: 5000 requests per hour

Rate limit headers are included in all responses:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1703545551
```

## Webhooks

The API supports webhooks for event notifications. To register a webhook:

```http
POST /webhooks
Authorization: Bearer your_jwt_token
Content-Type: application/json

{
    "url": "https://your-server.com/webhook",
    "events": ["agent.created", "task.completed"]
}
```

## SDKs and Client Libraries

Official SDKs are available for:
- Python: `pip install ai-agent-ecosystem`
- JavaScript: `npm install ai-agent-ecosystem`
- Go: `go get github.com/ai-agent-ecosystem/client-go`

## Examples

### Python Example

```python
from ai_agent_ecosystem import Client

# Initialize client
client = Client(api_key="your_api_key")

# Create an agent
agent = client.agents.create(
    name="My Agent",
    type="analytics",
    config={"setting": "value"}
)

# Create a task
task = client.tasks.create(
    agent_id=agent.id,
    type="analyze_data",
    data={"dataset": "sales_2024"}
)

# Wait for task completion
result = task.wait()
print(result)
```

### JavaScript Example

```javascript
const { Client } = require('ai-agent-ecosystem');

// Initialize client
const client = new Client({ apiKey: 'your_api_key' });

// Create an agent
async function createAgent() {
    const agent = await client.agents.create({
        name: 'My Agent',
        type: 'analytics',
        config: { setting: 'value' }
    });
    
    // Create a task
    const task = await client.tasks.create({
        agentId: agent.id,
        type: 'analyze_data',
        data: { dataset: 'sales_2024' }
    });
    
    // Wait for task completion
    const result = await task.wait();
    console.log(result);
}

createAgent();
```

## Support

For API support, please contact:
- Email: api-support@ai-agent-ecosystem.com
- Documentation: https://docs.ai-agent-ecosystem.com
- Status Page: https://status.ai-agent-ecosystem.com
