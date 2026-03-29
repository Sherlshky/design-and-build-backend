from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Record
from datetime import datetime, timedelta
import os

# Database connection
SQLALCHEMY_DATABASE_URL = "sqlite:///./main.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)


def create_mock_data():
    db = SessionLocal()
    try:
        # Create mock users
        users = [
            User(
                username="john_doe",
                password="hashed_password_1",
                face_image=b"123456",
                nickname="Johnny",
                exp=100,
                email="john@example.com",
            ),
            User(
                username="jane_smith",
                password="hashed_password_2",
                face_image=b"789012",
                nickname="Jane",
                exp=150,
                email="jane@example.com",
            ),
            User(
                username="bob_johnson",
                password="hashed_password_3",
                face_image=b"345678",
                nickname="Bobby",
                exp=75,
                email="bob@example.com",
            ),
            User(
                username="alice_williams",
                password="hashed_password_4",
                face_image=b"901234",
                nickname="Ali",
                exp=200,
                email="alice@example.com",
            ),
            User(
                username="charlie_brown",
                password="hashed_password_5",
                face_image=b"567890",
                nickname="Chuck",
                exp=125,
                email="charlie@example.com",
            ),
        ]
        db.add_all(users)
        db.commit()

        # Create mock records
        base_date = datetime.now().replace(hour=8, minute=30, second=0, microsecond=0)
        for i in range(10):
            username = users[i % 5].username
            timestamp = base_date + timedelta(days=i // 5, minutes=15 * (i % 5))
            record = Record(username=username, timestamp=timestamp)
            db.add(record)
        db.commit()

        print("Mock data has been successfully added to the database.")
    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_mock_data()


# Verify the data
def verify_data():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        records = db.query(Record).all()

        print("\nUsers:")
        for user in users:
            print(
                f"Username: {user.username}, Nickname: {user.nickname}, Exp: {user.exp}, Email: {user.email}"
            )

        print("\nRecords:")
        for record in records:
            print(f"Username: {record.username}, Timestamp: {record.timestamp}")
    finally:
        db.close()


if __name__ == "__main__":
    create_mock_data()
    verify_data()
