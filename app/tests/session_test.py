from app.db.session import SessionLocal
from sqlalchemy import text

def test_session():
    db = SessionLocal()
    result = db.execute(text("SELECT 1"))
    print("Session OK:", result.scalar())
    db.close()

if __name__ == "__main__":
    test_session()
