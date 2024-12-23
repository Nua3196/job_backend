import mysql.connector
import os
from dotenv import load_dotenv

def insert_data(table_name, data_dict):
    """
    데이터를 MySQL 테이블에 삽입하는 함수.
    
    Args:
        table_name (str): 데이터베이스 테이블 이름
        data_dict (dict): 삽입할 데이터 딕셔너리 (ID -> Name)
    """
    for key, value in data_dict.items():
        cursor.execute(f"""
            INSERT INTO {table_name} (id, name)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE name = VALUES(name)
        """, (key, value))
    db.commit()
    print(f"{table_name} 테이블에 데이터 삽입 완료.")

def fetch_data(table_name):
    """
    테이블 데이터를 조회하는 함수.
    
    Args:
        table_name (str): 데이터베이스 테이블 이름
    
    Returns:
        list: 테이블의 모든 데이터
    """
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    return rows

load_dotenv()

# MySQL 연결 설정
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
cursor = db.cursor()

# 데이터 정의
tech_data = {
    186: '라즈베리파이',
    320: '임베디드리눅스',
    195: 'Android',
    218: 'Flask'
}

location_data = {
    101000: '서울',
    108000: '인천',
    105000: '대전',
    113000: '전북'
}

# 데이터 삽입
insert_data('tech', tech_data)
insert_data('location', location_data)

# 데이터 확인
print("Tech 데이터:", fetch_data('tech'))
print("Location 데이터:", fetch_data('location'))