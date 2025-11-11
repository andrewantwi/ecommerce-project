from fastapi.security import OAuth2PasswordRequestForm
from schemas.user import UserOut, UserIn
from schemas.auth import TokenResponse, ForgotPasswordRequest, ResetPasswordRequest
from fastapi import APIRouter, Depends, Request, HTTPException
from starlette.responses import RedirectResponse, JSONResponse
from authlib.integrations.starlette_client import OAuth
import os
from dotenv import load_dotenv
from controller.auth import AuthController
from core.auth import create_access_token
import logging


load_dotenv()

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

oauth = OAuth()
oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url=os.getenv("GOOGLE_SERVER_METADATA_URL"),
    client_kwargs={'scope': 'openid email profile'}
)



@auth_router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return AuthController.login(form_data)

@auth_router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest):
    return AuthController.forgot_password(request)

@auth_router.post("/reset-password")
def reset_password(request: ResetPasswordRequest):
    return AuthController.reset_password(request)





@auth_router.get("/google/login")
async def google_login(request: Request):
    logging.info(f"Session: {request.session}")
    logging.info(f"Query params: {request.query_params}")
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@auth_router.get("/google/callback")
async def google_callback(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get("userinfo")
        if not user_info:
            raise HTTPException(status_code=400, detail="No user info from Google")

        user = AuthController.google_sign_in(user_info)
        jwt_token = create_access_token({"sub": user.email})

        return {
            "access_token": jwt_token,
            "token_type": "bearer",
            "expires_in": 3600,
            "user": {
                "email": user.email,
                "name": user_info.get("name"),
                "picture": user_info.get("picture")
            }
        }

    except Exception as e:
        logging.error(f"Google OAuth failed: {e}")
        raise HTTPException(status_code=400, detail="Authentication failed")