from dotenv import load_dotenv
import os


load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ACCESS_TOKEN_EXPIRE_MINUTES = 40
REFRESH_TOKEN_EXPIRE_DAYS = 2
ALGORITHMS = 'HS256'

class Settings:
    GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
    GITHUB_KEY = os.getenv('GITHUB_KEY')
    GITHUB_LOGIN_CALLBACK = 'http://127.0.0.1:8000/auth/github/login/callback/'

settings = Settings()


class Google:
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_KEY = os.getenv('GOOGLE_KEY')
    GOOGLE_LOGIN_CALLBACK = 'http://127.0.0.1:8000/auth/google/login/callback/'

google = Google()

