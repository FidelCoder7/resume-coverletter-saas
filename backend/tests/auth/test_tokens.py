from uuid import uuid4

from app.auth.tokens import (
    create_access_token,
    create_refresh_token,
    decode_token,
)


def test_create_access_token():
    user_id = uuid4()

    token = create_access_token(user_id)

    payload = decode_token(token)

    assert payload["sub"] == str(user_id)
    assert payload["type"] == "access"


def test_create_refresh_token():
    user_id = uuid4()

    token = create_refresh_token(user_id)

    payload = decode_token(token)

    assert payload["sub"] == str(user_id)
    assert payload["type"] == "refresh"
