import jwt
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

def generate_jwt(data):
    """
    JWT 토큰을 생성.
    - 데이터(payload)를 포함
    - 유효 기간(expiration)은 기본적으로 1시간
    """
    return jwt.encode(
        {"exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1), **data},
        SECRET_KEY,
        algorithm="HS256"
    )

def decode_jwt(token):
    """
    JWT 토큰을 검증 및 디코딩.
    - 유효하지 않거나 만료된 토큰은 None 반환
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
