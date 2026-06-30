from app.auth.security import hash_password, verify_password


def test_password_hash_is_not_plaintext():
    password = "SuperSecurePassword123!"

    hashed = hash_password(password)

    assert hashed != password


def test_verify_password_success():
    password = "SuperSecurePassword123!"

    hashed = hash_password(password)

    assert verify_password(password, hashed)


def test_verify_password_failure():
    password = "SuperSecurePassword123!"

    hashed = hash_password(password)

    assert not verify_password("WrongPassword", hashed)
