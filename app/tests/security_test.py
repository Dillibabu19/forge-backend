from app.core.security import hash_password, verify_password

def test_password_hashing():
    raw = "supersecret"
    hashed = hash_password(raw)

    assert raw != hashed
    assert verify_password(raw, hashed) is True
    assert verify_password("wrong", hashed) is False

if __name__ == "__main__":
    test_password_hashing()
    print("Security OK")
