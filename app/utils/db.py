import mysql.connector
from mysql.connector import pooling
from app.config import DATABASE_CONFIG

# 데이터베이스 연결 풀 생성
db_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=30,  # 풀 크기
    **DATABASE_CONFIG
)

def get_db():
    """
    데이터베이스 연결 객체를 반환.
    - 연결 풀에서 가져와 재사용.
    """
    try:
        return db_pool.get_connection()
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        raise
