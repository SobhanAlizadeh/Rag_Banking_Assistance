# tests/test_auth.py
from app.core.security import create_access_token, verify_token

def test_create_token():
    token = create_access_token({"user": "test"})
    assert token is not None
    assert isinstance(token, str)

def test_verify_token():
    token = create_access_token({"user": "test"})
    payload = verify_token(token)
    assert payload is not None
    assert payload.get("user") == "test"