import pytest
from datetime import datetime, timedelta
import jwt
from src.auth.auth import (
    create_access_token,
    verify_access_token,
    get_password_hash,
    verify_password,
    generate_api_key
)

@pytest.fixture
def user_data():
    """Sample user data for testing."""
    return {
        "id": "test123",
        "email": "test@example.com",
        "role": "user"
    }

@pytest.fixture
def secret_key():
    """Test secret key."""
    return "test_secret_key_12345"

def test_password_hashing():
    """Test password hashing and verification."""
    password = "test_password123"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrong_password", hashed)

def test_api_key_generation():
    """Test API key generation."""
    key = generate_api_key()
    assert len(key) == 32
    assert isinstance(key, str)
    
    # Generate multiple keys to ensure uniqueness
    keys = [generate_api_key() for _ in range(10)]
    assert len(set(keys)) == 10

def test_access_token_creation(user_data, secret_key):
    """Test access token creation."""
    token = create_access_token(
        data=user_data,
        secret_key=secret_key,
        expires_delta=timedelta(minutes=15)
    )
    
    assert isinstance(token, str)
    decoded = jwt.decode(token, secret_key, algorithms=["HS256"])
    
    assert decoded["sub"] == user_data["id"]
    assert decoded["email"] == user_data["email"]
    assert decoded["role"] == user_data["role"]
    assert "exp" in decoded

def test_access_token_verification(user_data, secret_key):
    """Test access token verification."""
    token = create_access_token(
        data=user_data,
        secret_key=secret_key,
        expires_delta=timedelta(minutes=15)
    )
    
    decoded = verify_access_token(token, secret_key)
    assert decoded["sub"] == user_data["id"]
    assert decoded["email"] == user_data["email"]
    
def test_expired_token(user_data, secret_key):
    """Test handling of expired tokens."""
    token = create_access_token(
        data=user_data,
        secret_key=secret_key,
        expires_delta=timedelta(microseconds=1)
    )
    
    # Wait for token to expire
    import time
    time.sleep(0.1)
    
    with pytest.raises(jwt.ExpiredSignatureError):
        verify_access_token(token, secret_key)

def test_invalid_token(secret_key):
    """Test handling of invalid tokens."""
    with pytest.raises(jwt.InvalidTokenError):
        verify_access_token("invalid_token", secret_key)
    
def test_token_with_wrong_secret(user_data, secret_key):
    """Test token verification with wrong secret key."""
    token = create_access_token(
        data=user_data,
        secret_key=secret_key,
        expires_delta=timedelta(minutes=15)
    )
    
    wrong_secret = "wrong_secret_key"
    with pytest.raises(jwt.InvalidSignatureError):
        verify_access_token(token, wrong_secret)

def test_token_without_expiry(user_data, secret_key):
    """Test token creation without expiry time."""
    token = create_access_token(
        data=user_data,
        secret_key=secret_key
    )
    
    decoded = verify_access_token(token, secret_key)
    assert decoded["sub"] == user_data["id"]
    assert "exp" in decoded

def test_password_hash_uniqueness():
    """Test that same password generates different hashes."""
    password = "test_password123"
    hash1 = get_password_hash(password)
    hash2 = get_password_hash(password)
    
    assert hash1 != hash2
    assert verify_password(password, hash1)
    assert verify_password(password, hash2)

def test_api_key_format():
    """Test API key format and characteristics."""
    key = generate_api_key()
    
    # Check length
    assert len(key) == 32
    
    # Check character set (hexadecimal)
    assert all(c in "0123456789abcdef" for c in key.lower())
    
    # Check randomness (basic entropy check)
    char_counts = {}
    for char in key.lower():
        char_counts[char] = char_counts.get(char, 0) + 1
    
    # No character should appear too many times
    assert all(count < 10 for count in char_counts.values())
