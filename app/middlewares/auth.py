from functools import wraps

def jwt_required(required_roles=None):
    """
    JWT 인증 및 권한 검사 미들웨어
    Args:
        required_roles (list, optional): 허용된 역할 목록 (예: ['admin', 'employer']). 기본값은 None.
    """
    def decorator(func):
        @wraps(func) # wraps 적용으로 함수 이름 유지지
        def wrapper(*args, **kwargs):
            # Authorization 헤더 확인
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({"error": "Authorization header is required"}), 401

            # 토큰 검증
            token = auth_header.split(" ")[1]
            decoded_token = decode_token(token)

            if not decoded_token:
                return jsonify({"error": "Invalid or expired token"}), 401

            # 역할 확인
            if required_roles and decoded_token.get('role') not in required_roles:
                return jsonify({"error": "Permission denied"}), 403

            # 사용자 정보 추가
            request.user = decoded_token
            return func(*args, **kwargs)
        return wrapper
    return decorator
