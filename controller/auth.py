from fastapi import HTTPException
from utils.session import SessionManager as DBSession
from core.auth import verify_password, create_access_token
from models.user import User


class AuthController:

    @staticmethod
    def login(form_data):
        try:
            with DBSession() as db:
                user = db.query(User).filter(User.email == form_data.username).first()
                if not user or not verify_password(form_data.password, user.hashed_password):
                    raise HTTPException(status_code=401, detail="Invalid credentials")

                token = create_access_token({"sub": user.email})
                return {"access_token": token, "token_type": "bearer"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error logging in: {str(e)}")

    @staticmethod
    def google_sign_in(user_info):
        with DBSession() as db:
            user = db.query(User).filter(User.email == user_info["email"]).first()
            if not user:
                user = User(
                    full_name=user_info.get("name"),
                    email=user_info.get("email"),
                    hashed_password="",  # Not used for Google accounts
                    is_active=True,
                    is_owner=False
                )
                db.add(user)
                db.commit()
                db.refresh(user)
            return user
