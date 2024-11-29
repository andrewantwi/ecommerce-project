from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Session

from core.setup import Base
from schemas.user import UserIn, UserUpdate


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    created_at = Column(String, default=datetime.now().isoformat())

    reviews = relationship('Review', back_populates='user')

    def __str__(self) -> str:
        self.username

    @staticmethod
    def extract_username(email: str):
        return email.split('@')[0]

    @classmethod
    def validate_id(cls, user_id: int, db: Session):
        if not db.query(cls).filter(cls.id == user_id).first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='User not found')
        return True

    @classmethod
    def validate_password(cls, password: str, db: Session):
        if len(password) < 6:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Password must be at least 6 characters')

    @classmethod
    def validate_email(cls, email: str, db: Session):
        if db.query(cls).filter(cls.email == email).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Email already registered')

    @classmethod
    def validate_user(cls, user: UserIn, db: Session):
        cls.validate_email(user.email, db)
        cls.validate_password(user.password, db)
        return user

    @classmethod
    def get_users(cls, db: Session):
        return db.query(cls).all()

    @classmethod
    def get_user(cls, user_id: int, db: Session):
        return db.query(cls).filter(cls.id == user_id).first()

    @classmethod
    def create_user(cls, user: UserIn, db: Session):
        username = cls.extract_username(user.email)
        user = cls(**user.dict(), username=username)
        db.add(user)
        return user

    @classmethod
    def update_user(cls, user_id: int, update_data: UserUpdate, db: Session):
        user = db.query(cls).filter(cls.id == user_id).first()
        user.username = update_data.username
        user.password = update_data.password
        return user

    @classmethod
    def delete_user(cls, user_id: int, db: Session):
        user = db.query(cls).filter(cls.id == user_id).first()
        db.delete(user)
        return user
