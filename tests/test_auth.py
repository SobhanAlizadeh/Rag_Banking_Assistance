from app.core.security import create_access_token, verify_token

def test_jwt():
    token = create_access_token({"user": "admin"})
    payload = verify_token(token)
    assert payload["user"] == "admin"