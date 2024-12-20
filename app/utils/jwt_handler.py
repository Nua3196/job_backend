import jwt
import datetime
from app.config import SECRET_KEY, REFRESH_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRES, JWT_REFRESH_TOKEN_EXPIRES

def generate_access_token(payload):
    """
    Access 토큰 생성
    """
    try:
        payload['exp'] = datetime.datetime.utcnow() + JWT_ACCESS_TOKEN_EXPIRES
        return jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    except Exception as e:
        raise ValueError(f"Error generating access token: {e}")

def generate_refresh_token(payload):
    """
    Refresh 토큰 생성
    """
    try:
        payload['exp'] = datetime.datetime.utcnow() + JWT_REFRESH_TOKEN_EXPIRES
        return jwt.encode(payload, REFRESH_SECRET_KEY, algorithm='HS256')
    except Exception as e:
        raise ValueError(f"Error generating refresh token: {e}")

def decode_token(token, is_refresh=False):
    """
    토큰 검증 및 디코딩
    """
    try:
        secret_key = REFRESH_SECRET_KEY if is_refresh else SECRET_KEY
        return jwt.decode(token, secret_key, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}
    except Exception as e:
        print(f"Unexpected error during token decoding: {str(e)}")
        return {"error": "Decoding failed"}
