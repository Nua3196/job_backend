import os
from dotenv import load_dotenv

load_dotenv()

# Flask 기본 설정
SECRET_KEY = os.getenv('SECRET_KEY')  # Access 토큰 서명 키
REFRESH_SECRET_KEY = os.getenv('REFRESH_SECRET_KEY')  # Refresh 토큰 서명 키

# JWT 설정
JWT_ACCESS_TOKEN_EXPIRES = 1  # Access 토큰 만료 시간 (단위: 시간)
JWT_REFRESH_TOKEN_EXPIRES = 24 * 7  # Refresh 토큰 만료 시간 (단위: 시간)

# 데이터베이스 설정
DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}
