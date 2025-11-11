import os

from dotenv import load_dotenv
from fastapi import HTTPException

from schemas.auth import ResetPasswordRequest, ForgotPasswordRequest
from utils.session import SessionManager as DBSession
from core.auth import verify_password, create_access_token, hash_password
from models.user import User
from core.mailer import send_reset_email
from datetime import datetime, timedelta
from jose import jwt, JWTError

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
frontend_url = os.getenv("FRONTEND_URL")
ALGORITHM = os.getenv("ALGORITHM")
RESET_TOKEN_EXPIRE_MINUTES = 15

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
                    hashed_password="",
                    is_active=True,
                    is_owner=False
                )
                db.add(user)
                db.commit()
                db.refresh(user)
            return user

    @staticmethod
    def forgot_password(request: ForgotPasswordRequest):
        with DBSession() as db:
            user = db.query(User).filter(User.email == request.email).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            expire = datetime.utcnow() + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
            token_data = {"sub": user.email, "exp": expire}
            token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

            reset_link = f"{frontend_url}/reset-password?token={token}"
            send_reset_email(user.email, reset_link)
            return {"message": "Password reset email sent"}

    @staticmethod
    def reset_password(request: ResetPasswordRequest):
        try:
            payload = jwt.decode(request.token, SECRET_KEY, algorithms=[ALGORITHM])
            email = payload.get("sub")
        except JWTError:
            raise HTTPException(status_code=400, detail="Invalid or expired token")

        with DBSession() as db:
            user = db.query(User).filter(User.email == email).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            user.hashed_password = hash_password(request.new_password)
            db.commit()
            return {"message": "Password reset successful"}
