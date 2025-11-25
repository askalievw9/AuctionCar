from auction_car.config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS, ALGORITHMS
from jose import jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta, datetime
from auction_car.db.database import SessionLocal
from typing import Optional
from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from starlette.requests import Request
from auction_car.config import settings, google
from authlib.integrations.starlette_client import OAuth


oauth = OAuth()
oauth.register(
    name='github',
    client_id=settings.GITHUB_CLIENT_ID,
    client_secret=settings.GITHUB_KEY,
    authorize_url='https://github.com/login/oauth/authorize'
)


oauth.register(
    name='google',
    client_id=google.GOOGLE_CLIENT_ID,
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    client_kwargs={"scope": "openid profile email"},
)


social_auth = APIRouter(prefix='/auth', tags=['SocialAuth'])


oauth2_schema = OAuth2PasswordBearer(tokenUrl='/auth/login/')
password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHMS)


def create_refresh_token(data: dict):
    return create_access_token(data, expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))


def verify_password(plain_password, hash_password):
    return password_context.verify(plain_password, hash_password)


def get_password_hash(password):
    return password_context.hash(password)
@social_auth.get('/github/')
async def github_login(request: Request):
    redirect_uri = settings.GITHUB_LOGIN_CALLBACK
    return await oauth.github.authorize_redirect(request, redirect_uri)


@social_auth.get('/google/')
async def google_login(request: Request):
    redirect_uri = google.GOOGLE_LOGIN_CALLBACK
    return await oauth.google.authorize_redirect(request, redirect_uri)