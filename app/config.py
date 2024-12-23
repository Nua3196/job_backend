import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

# Flask 기본 설정
SECRET_KEY = os.getenv('SECRET_KEY')
REFRESH_SECRET_KEY = os.getenv('REFRESH_SECRET_KEY')

if not SECRET_KEY or not REFRESH_SECRET_KEY:
    raise ValueError("SECRET_KEY and REFRESH_SECRET_KEY must be set in the environment")

# JWT 설정
try:
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES')))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES')))
except (TypeError, ValueError):
    raise ValueError("JWT_ACCESS_TOKEN_EXPIRES and JWT_REFRESH_TOKEN_EXPIRES must be valid integers")

# 데이터베이스 설정
DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
}

if not all(DATABASE_CONFIG.values()):
    raise ValueError("DATABASE_CONFIG variables (host, user, password, database) must be set in the environment")
