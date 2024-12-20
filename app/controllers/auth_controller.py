from flask import Blueprint, jsonify, request
from app.models.user_model import User
from app.utils.jwt_handler import generate_access_token, generate_refresh_token, decode_token

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/signup', methods=['POST'])
def signup():
    """
    회원가입 API
    - 요청 데이터(JSON): email, password, role, company
    - 사용자 추가 후 성공/실패 메시지 반환
    """
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'applicant')  # 기본 역할은 'applicant'
        company = data.get('company')  # 선택적 필드

        # 필수 입력값 검증
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        # 이메일 형식 검증
        if not User.is_valid_email(email):
            return jsonify({"error": "Invalid email format"}), 400

        # 역할(role) 검증
        if role not in ['admin', 'applicant', 'employer']:
            return jsonify({"error": f"Invalid role: {role}"}), 400

        # 사용자 추가
        result = User.add_user(email, password, role, company)
        if "error" in result:
            return jsonify(result), 400

        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    사용자 로그인 처리
    - Access 토큰과 Refresh 토큰을 생성하여 반환
    """
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        # 사용자 인증
        user = User.authenticate(email, password)
        if user:
            payload = {"id": user.id, "email": user.email, "role": user.role}
            access_token = generate_access_token(payload)
            refresh_token = generate_refresh_token(payload)
            return jsonify({
                "message": "Login successful",
                "access_token": access_token,
                "refresh_token": refresh_token
            }), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    """
    Refresh 토큰을 사용해 새로운 Access 토큰 발급
    """
    try:
        data = request.json
        refresh_token = data.get('refresh_token')

        if not refresh_token:
            return jsonify({"error": "Refresh token is required"}), 400

        # Refresh 토큰 검증
        decoded_payload = decode_token(refresh_token, is_refresh=True)
        if not decoded_payload:
            return jsonify({"error": "Invalid or expired refresh token"}), 401

        # 필수 키 검증
        required_keys = {"id", "email", "role"}
        if not required_keys.issubset(decoded_payload.keys()):
            return jsonify({"error": "Invalid token payload"}), 400

        # 새로운 Access 토큰 발급
        access_token = generate_access_token({
            "id": decoded_payload['id'],
            "email": decoded_payload['email'],
            "role": decoded_payload['role']
        })
        return jsonify({"access_token": access_token}), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

from flask import Blueprint, jsonify, request
from app.models.user_model import User
from app.utils.jwt_handler import decode_token

@auth_bp.route('/profile', methods=['PUT'])
def update_profile():
    """
    회원 정보 수정 API
    - 요청 데이터(JSON): password, role
    - JWT 토큰에서 사용자 ID 추출 후 해당 사용자 정보 수정
    """
    try:
        # JWT 토큰 검증 및 사용자 ID 추출
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization header is required"}), 401

        token = auth_header.split(" ")[1]
        decoded_token = decode_token(token)

        if not decoded_token:
            return jsonify({"error": "Invalid or expired token"}), 401

        user_id = decoded_token.get('id')
        if not user_id:
            return jsonify({"error": "Invalid token payload"}), 400

        # 요청 데이터
        data = request.json
        password = data.get('password')
        role = data.get('role')

        # 역할 변경 권한 확인 (관리자만 가능)
        if role and decoded_token.get('role') != 'admin':
            return jsonify({"error": "Permission denied to change role"}), 403

        # 사용자 정보 업데이트
        update_fields = {}
        if password:
            update_fields['password'] = User.encode_password(password)
        if role:
            update_fields['role'] = role

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        result = User.update_user(user_id, update_fields)
        if "error" in result:
            return jsonify(result), 400

        return jsonify({"message": "User profile updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@auth_bp.route('/delete', methods=['DELETE'])
def delete_account():
    """
    회원 탈퇴 API
    - JWT 토큰에서 사용자 ID를 추출하여 해당 계정 삭제
    """
    try:
        # JWT 토큰 검증 및 사용자 ID 추출
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization header is required"}), 401

        token = auth_header.split(" ")[1]
        decoded_token = decode_token(token)

        if not decoded_token:
            return jsonify({"error": "Invalid or expired token"}), 401

        user_id = decoded_token.get('id')
        if not user_id:
            return jsonify({"error": "Invalid token payload"}), 400

        # 사용자 삭제
        result = User.delete_user(user_id)
        if "error" in result:
            return jsonify(result), 400

        return jsonify({"message": "User account deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
