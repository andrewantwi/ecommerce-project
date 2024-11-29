from models.user import User
from schemas.user import UserIn, UserUpdate
from utils.session import SessionManager as DBSession


class UserController:

    @staticmethod
    def get_users():
        with DBSession() as db:
            users = User.get_users(db)
            return users

    @staticmethod
    def get_user(user_id: int):
        with DBSession() as db:
            user = User.validate_id(user_id, db)
            return user

    @staticmethod
    def create_user(user: UserIn):
        with DBSession() as db:
            User.validate_user(user, db)
            user = User.create_user(user, db)
            db.commit()
            db.refresh(user)
            return user

    @staticmethod
    def update_user(user_id: int, update_data: UserUpdate):
        with DBSession() as db:
            User.validate_id(user_id, db)
            user = User.update_user(user_id, update_data, db)
            db.commit()
            db.refresh(user)
            return user

    @staticmethod
    def delete_user(user_id: int):
        with DBSession() as db:
            User.validate_id(user_id, db)
            user = User.delete_user(user_id, db)
            db.commit()
            return user
