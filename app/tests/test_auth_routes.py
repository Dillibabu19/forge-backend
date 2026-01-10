from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.db.session import SessionLocal
from app.models.user import User

client = TestClient(app)


def cleanup_user(email: str):
    db: Session = SessionLocal()
    try:
        db.query(User).filter(User.email == email).delete()
        db.commit()
    finally:
        db.close()


def test_signup_and_login():
    email = "route_test@example.com"
    password = "strongpassword123"

    # ensure clean state
    cleanup_user(email)

    # ---------- SIGNUP ----------
    signup_res = client.post(
        "/auth/signup",
        json={
            "email": email,
            "password": password,
        },
    )

    assert signup_res.status_code == 200
    assert signup_res.json()["success"] is True

    # ---------- LOGIN ----------
    login_res = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert login_res.status_code == 200
    assert login_res.json()["success"] is True

    # cleanup
    cleanup_user(email)