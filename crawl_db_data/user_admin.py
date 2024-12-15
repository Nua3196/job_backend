import mysql.connector
import base64
import os  # Salt 생성
from dotenv import load_dotenv
import re

load_dotenv()

# MySQL 연결 설정
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
cursor = db.cursor()

def encode_password(password):
    """
    비밀번호를 Base64로 인코딩하는 함수.

    Args:
        password (str): 평문 비밀번호

    Returns:
        str: Base64로 인코딩된 비밀번호
    """
    salt = os.urandom(16)  # 16바이트 랜덤 Salt 생성
    salted_password = salt + password.encode('utf-8')  # Salt 추가
    return base64.b64encode(salted_password).decode('utf-8')

def is_valid_email(email):
    """
    이메일 형식을 검증하는 함수.

    Args:
        email (str): 입력된 이메일

    Returns:
        bool: 이메일이 유효하면 True, 그렇지 않으면 False
    """
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(email_regex, email) is not None

def add_user(email, password, role, company=None):
    """
    사용자를 user 테이블에 추가하거나 기존 사용자 ID를 반환하는 범용 함수.

    Args:
        email (str): 사용자 이메일
        password (str): 평문 비밀번호
        role (str): 사용자 역할 ('admin', 'creator', 'applicant' 등)
        company (int, optional): 회사 ID (기본값: None)

    Returns:
        int: 사용자 ID
    """
    # 이메일 형식 검증
    if not is_valid_email(email):
        raise ValueError(f"유효하지 않은 이메일 형식입니다: {email}")

    # 이미 존재하는 이메일인지 확인
    cursor.execute("SELECT id FROM user WHERE email = %s", (email,))
    result = cursor.fetchone()

    if result:
        print(f"사용자 {email}은(는) 이미 존재합니다. ID: {result[0]}")
        return result[0]

    # 비밀번호 Base64 인코딩
    encoded_password = encode_password(password)

    # 사용자 추가
    cursor.execute("""
        INSERT INTO user (email, password, role, company)
        VALUES (%s, %s, %s, %s)
    """, (email, encoded_password, role, company))
    db.commit()

    user_id = cursor.lastrowid
    print(f"사용자 {email} 추가 완료. ID: {user_id}")
    return user_id

# 스크립트 실행
if __name__ == "__main__":
    # # 사용자 정보
    # user_info = {
    #     "email": "mytale3@gmail.com",
    #     "password": "wsd@19462",  # 평문 비밀번호
    #     "role": "admin",
    #     "company": None  # 관리자는 회사와 무관
    # }

    # # 사용자 추가
    # admin_id = add_user(**user_info)
    # print(f"관리자 ID: {admin_id}")
