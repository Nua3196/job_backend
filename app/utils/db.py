import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_db():
    """
    데이터베이스 연결 객체를 생성 및 반환.
    - MySQL 데이터베이스 연결 설정
    """
    db = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    return db
