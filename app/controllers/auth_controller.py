from flask import Blueprint, jsonify, request
from app.models.user_model import User
from app.utils.jwt_handler import generate_access_token, generate_refresh_token, decode_token
from app.utils.redis_client import add_to_blacklist, is_token_blacklisted
from app.middlewares.auth import jwt_required

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    ---
    tags:
      - Auth
    summary: "User Logout"
    description: "Logs out a user by invalidating the provided refresh token."
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              refresh_token:
                type: string
                description: "The refresh token to invalidate."
    responses:
      200:
        description: "User logged out successfully."
      400:
        description: "Refresh token is missing or invalid."
      500:
        description: "Internal server error."
    """
    try:
        data = request.json
        refresh_token = data.get('refresh_token')

        if not refresh_token:
            return jsonify({"error": "Refresh token is required"}), 400

        # Refresh Token 블랙리스트 추가
        add_to_blacklist(refresh_token)
        return jsonify({"message": "Logged out successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@auth_bp.route('/signup', methods=['POST'])
def signup():
    """
    ---
    tags:
      - Auth
    summary: "User Signup"
    description: "Creates a new user account."
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              email:
                type: string
              password:
                type: string
              role:
                type: string
                enum: ["admin", "employer", "applicant"]
              company_name:
                type: string
                description: "Required if the role is employer."
              company_link:
                type: string
                description: "Required if the role is employer."
    responses:
      201:
        description: "User created successfully."
      400:
        description: "Validation error."
      500:
        description: "Internal server error."
    """
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'applicant')  # 기본 역할은 'applicant'

        # 필수 입력값 검증
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        # 이메일 형식 검증
        if not User.is_valid_email(email):
            return jsonify({"error": "Invalid email format"}), 400

        # 역할(role) 검증
        if role not in ['admin', 'applicant', 'employer']:
            return jsonify({"error": f"Invalid role: {role}"}), 400

        company_id = None  # 기본 회사 ID는 None

        if role == 'employer':
            # 회사 이름 및 링크 입력 확인
            company_name = data.get('company_name')
            company_link = data.get('company_link')
            if not company_name or not company_link:
                return jsonify({"error": "Company name and link are required for employers"}), 400

            # 회사 정보 확인 또는 생성
            company_id = Company.get_or_create(company_name, company_link)

        # 사용자 추가
        result = User.add_user(email, password, role, company_id)
        if "error" in result:
            return jsonify(result), 400

        return jsonify(result), 201

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    ---
    tags:
      - Auth
    summary: "User Login"
    description: "Logs in a user and provides access and refresh tokens."
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              email:
                type: string
              password:
                type: string
    responses:
      200:
        description: "Login successful."
      401:
        description: "Invalid credentials."
      500:
        description: "Internal server error."
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
            payload = {"id": user.id, "email": user.email, "role": user.role, "company": user.company}
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
    ---
    tags:
      - Auth
    summary: "Token Refresh"
    description: "Refreshes the access token using a valid refresh token."
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              refresh_token:
                type: string
                description: "The refresh token to use for generating a new access token."
    responses:
      200:
        description: "New access token generated."
      403:
        description: "Token is blacklisted."
      401:
        description: "Invalid or expired refresh token."
      500:
        description: "Internal server error."
    """
    try:
        data = request.json
        refresh_token = data.get('refresh_token')

        if not refresh_token:
            return jsonify({"error": "Refresh token is required"}), 400

        # 블랙리스트 확인
        if is_token_blacklisted(refresh_token):
            return jsonify({"error": "This token has been logged out"}), 403

        # Refresh Token 검증
        decoded_token = decode_token(refresh_token, is_refresh=True)
        if not decoded_token:
            return jsonify({"error": "Invalid or expired refresh token"}), 401

        # 새로운 Access 토큰 발급
        access_token = generate_access_token({
            "id": decoded_token['id'],
            "email": decoded_token['email'],
            "role": decoded_token['role']
        })
        return jsonify({"access_token": access_token}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500