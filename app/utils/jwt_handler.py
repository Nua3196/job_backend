import jwt
import datetime
from app.config import SECRET_KEY, REFRESH_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRES, JWT_REFRESH_TOKEN_EXPIRES

def generate_access_token(payload):
    """
    Access 토큰 생성
    - 사용자 정보를 포함한 JWT 토큰 생성
    - 유효 기간(expiration)은 설정 파일에서 지정

    Args:
        payload (dict): 토큰에 포함될 사용자 정보

    Returns:
        str: 생성된 Access 토큰
    """
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(hours=JWT_ACCESS_TOKEN_EXPIRES)
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def generate_refresh_token(payload):
    """
    Refresh 토큰 생성
    - 사용자 정보를 포함한 JWT 토큰 생성
    - Refresh 토큰은 Access 토큰을 재발급받기 위해 사용
    - 유효 기간(expiration)은 설정 파일에서 지정

    Args:
        payload (dict): 토큰에 포함될 사용자 정보

    Returns:
        str: 생성된 Refresh 토큰
    """
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(hours=JWT_REFRESH_TOKEN_EXPIRES)
    return jwt.encode(payload, REFRESH_SECRET_KEY, algorithm='HS256')

def decode_token(token, is_refresh=False):
    """
    토큰 검증 및 디코딩
    - Access 토큰과 Refresh 토큰을 구분하여 검증
    - 유효하지 않거나 만료된 토큰은 None 반환

    Args:
        token (str): 검증할 토큰
        is_refresh (bool): Refresh 토큰 여부

    Returns:
        dict: 디코딩된 사용자 정보
        None: 유효하지 않거나 만료된 토큰
    """
    try:
        secret_key = REFRESH_SECRET_KEY if is_refresh else SECRET_KEY
        return jwt.decode(token, secret_key, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
