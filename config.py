import os
from dotenv import load_dotenv

load_dotenv()

# Flask 기본 설정
SECRET_KEY = os.getenv('SECRET_KEY')  # 기본 암호화 키

# 데이터베이스 설정
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')