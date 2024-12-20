import mysql.connector
from app.config import DATABASE_CONFIG

def get_db():
    """
    데이터베이스 연결 객체를 생성 및 반환.
    - `config.py`의 DATABASE_CONFIG를 사용
    """
    db = mysql.connector.connect(**DATABASE_CONFIG)
    return db
