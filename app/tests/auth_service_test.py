from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.services.auth_service import AuthService
from app.models.user import User
from app.core.security import verify_password


def test_create_user():
    db: Session = SessionLocal()

    try:
        email = "test_user@example.com"
        password = "password@123"

        user = AuthService.create_user(
            db,
            email=email,
            password=password,
        )

        # basic assertions
        assert user.id is not None
        assert user.email == email
        assert user.password_hash != password
        assert verify_password(password, user.password_hash) is True

        # verify user exists in DB
        db_user = db.query(User).filter(User.email == email).first()
        assert db_user is not None
        assert db_user.id == user.id

        print("create_user OK")

    finally:
        # cleanup (important for repeatable tests)
        db.query(User).filter(User.email == email).delete()
        db.commit()
        db.close()
        
def test_authenticate_user():
    db: Session = SessionLocal()

    try:
        email = "login_test@example.com"
        password = "secret123"

        # create user first
        user = AuthService.create_user(
            db,
            email=email,
            password=password,
        )

        # authenticate
        auth_user = AuthService.authenticate_user(
            db,
            email=email,
            password=password,
        )

        assert auth_user.id == user.id
        assert auth_user.email == email

        print("authenticate_user OK")

    finally:
        db.query(User).filter(User.email == email).delete()
        db.commit()
        db.close()


if __name__ == "__main__":
    test_create_user()
    test_authenticate_user()
