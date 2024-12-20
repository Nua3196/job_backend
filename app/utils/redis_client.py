from redis import Redis

redis_client = Redis(host='localhost', port=6379, decode_responses=True)

def add_to_blacklist(token, expiry=3600 * 24 * 7):
    """
    블랙리스트에 토큰 추가
    Args:
        token (str): 무효화할 Refresh Token
        expiry (int): 만료 시간(초)
    """
    redis_client.set(token, "blacklisted", ex=expiry)

def is_token_blacklisted(token):
    """
    블랙리스트 여부 확인
    Args:
        token (str): 확인할 Refresh Token
    Returns:
        bool: 블랙리스트에 있으면 True, 없으면 False
    """
    return redis_client.get(token) is not None
