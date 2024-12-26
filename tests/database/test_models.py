import pytest
from datetime import datetime
from sqlalchemy.orm import Session
from src.database.models import (
    User,
    APIKey,
    Agent,
    AgentMetric,
    Task,
    Revenue,
    MarketplaceItem,
    Base
)
from src.database.database import engine, SessionLocal

@pytest.fixture(scope="function")
def db():
    """Create test database and yield session."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def user(db: Session):
    """Create test user."""
    user = User(
        email="test@example.com",
        hashed_password="hashed_password",
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def api_key(db: Session, user: User):
    """Create test API key."""
    api_key = APIKey(
        key="test_key_123",
        user_id=user.id,
        is_active=True
    )
    db.add(api_key)
    db.commit()
    db.refresh(api_key)
    return api_key

@pytest.fixture
def agent(db: Session):
    """Create test agent."""
    agent = Agent(
        name="test_agent",
        type="test",
        status="active",
        config={"test": True}
    )
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent

def test_user_creation(db: Session):
    """Test user model creation."""
    user = User(
        email="test@example.com",
        hashed_password="hashed_password",
        is_active=True
    )
    db.add(user)
    db.commit()
    
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.is_active
    assert user.created_at is not None
    
def test_api_key_creation(db: Session, user: User):
    """Test API key model creation."""
    api_key = APIKey(
        key="test_key_123",
        user_id=user.id,
        is_active=True
    )
    db.add(api_key)
    db.commit()
    
    assert api_key.id is not None
    assert api_key.key == "test_key_123"
    assert api_key.user_id == user.id
    assert api_key.is_active
    assert api_key.created_at is not None
    
def test_agent_creation(db: Session):
    """Test agent model creation."""
    agent = Agent(
        name="test_agent",
        type="test",
        status="active",
        config={"test": True}
    )
    db.add(agent)
    db.commit()
    
    assert agent.id is not None
    assert agent.name == "test_agent"
    assert agent.type == "test"
    assert agent.status == "active"
    assert agent.config == {"test": True}
    assert agent.created_at is not None
    
def test_agent_metric_creation(db: Session, agent: Agent):
    """Test agent metric model creation."""
    metric = AgentMetric(
        agent_id=agent.id,
        metric_type="performance",
        value=95.5,
        timestamp=datetime.utcnow()
    )
    db.add(metric)
    db.commit()
    
    assert metric.id is not None
    assert metric.agent_id == agent.id
    assert metric.metric_type == "performance"
    assert metric.value == 95.5
    assert metric.timestamp is not None
    
def test_task_creation(db: Session, agent: Agent):
    """Test task model creation."""
    task = Task(
        agent_id=agent.id,
        type="test_task",
        status="pending",
        data={"test": True}
    )
    db.add(task)
    db.commit()
    
    assert task.id is not None
    assert task.agent_id == agent.id
    assert task.type == "test_task"
    assert task.status == "pending"
    assert task.data == {"test": True}
    assert task.created_at is not None
    
def test_revenue_creation(db: Session):
    """Test revenue model creation."""
    revenue = Revenue(
        amount=100.50,
        currency="USD",
        source="subscription",
        timestamp=datetime.utcnow()
    )
    db.add(revenue)
    db.commit()
    
    assert revenue.id is not None
    assert revenue.amount == 100.50
    assert revenue.currency == "USD"
    assert revenue.source == "subscription"
    assert revenue.timestamp is not None
    
def test_marketplace_item_creation(db: Session, user: User):
    """Test marketplace item model creation."""
    item = MarketplaceItem(
        seller_id=user.id,
        name="Test Item",
        description="Test Description",
        price=99.99,
        category="test",
        status="active"
    )
    db.add(item)
    db.commit()
    
    assert item.id is not None
    assert item.seller_id == user.id
    assert item.name == "Test Item"
    assert item.description == "Test Description"
    assert item.price == 99.99
    assert item.category == "test"
    assert item.status == "active"
    assert item.created_at is not None
    
def test_user_api_keys_relationship(db: Session, user: User, api_key: APIKey):
    """Test relationship between user and API keys."""
    assert len(user.api_keys) == 1
    assert user.api_keys[0].key == api_key.key
    
def test_agent_metrics_relationship(db: Session, agent: Agent):
    """Test relationship between agent and metrics."""
    metric = AgentMetric(
        agent_id=agent.id,
        metric_type="performance",
        value=95.5,
        timestamp=datetime.utcnow()
    )
    db.add(metric)
    db.commit()
    
    assert len(agent.metrics) == 1
    assert agent.metrics[0].value == 95.5
    
def test_agent_tasks_relationship(db: Session, agent: Agent):
    """Test relationship between agent and tasks."""
    task = Task(
        agent_id=agent.id,
        type="test_task",
        status="pending",
        data={"test": True}
    )
    db.add(task)
    db.commit()
    
    assert len(agent.tasks) == 1
    assert agent.tasks[0].type == "test_task"
    
def test_user_marketplace_items_relationship(db: Session, user: User):
    """Test relationship between user and marketplace items."""
    item = MarketplaceItem(
        seller_id=user.id,
        name="Test Item",
        description="Test Description",
        price=99.99,
        category="test",
        status="active"
    )
    db.add(item)
    db.commit()
    
    assert len(user.marketplace_items) == 1
    assert user.marketplace_items[0].name == "Test Item"
    
def test_cascade_delete_user(db: Session, user: User, api_key: APIKey):
    """Test cascade deletion of user and related records."""
    user_id = user.id
    db.delete(user)
    db.commit()
    
    assert db.query(User).filter_by(id=user_id).first() is None
    assert db.query(APIKey).filter_by(user_id=user_id).first() is None
    
def test_cascade_delete_agent(db: Session, agent: Agent):
    """Test cascade deletion of agent and related records."""
    agent_id = agent.id
    
    # Create related records
    metric = AgentMetric(
        agent_id=agent.id,
        metric_type="performance",
        value=95.5,
        timestamp=datetime.utcnow()
    )
    task = Task(
        agent_id=agent.id,
        type="test_task",
        status="pending",
        data={"test": True}
    )
    db.add_all([metric, task])
    db.commit()
    
    # Delete agent
    db.delete(agent)
    db.commit()
    
    assert db.query(Agent).filter_by(id=agent_id).first() is None
    assert db.query(AgentMetric).filter_by(agent_id=agent_id).first() is None
    assert db.query(Task).filter_by(agent_id=agent_id).first() is None
