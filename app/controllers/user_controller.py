from flask import Blueprint, jsonify, request
from app.models.user_model import User
from app.middlewares.auth import jwt_required

user_bp = Blueprint('user', __name__, url_prefix='/api/users')

@user_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()  # JWT 인증 필요
def get_user_details(user_id):
    """
    ---
    tags:
      - Users
    summary: "Get User Details"
    description: "Retrieve details of a specific user by their ID."
    parameters:
      - in: path
        name: user_id
        required: true
        schema:
          type: integer
        description: "The ID of the user to retrieve."
    responses:
      200:
        description: "User details retrieved successfully."
      403:
        description: "Permission denied."
      404:
        description: "User not found."
      500:
        description: "Internal server error."
    """
    try:
        current_user_id = request.user['id']
        current_user_role = request.user['role']

        # 자기 자신의 정보 또는 관리자의 요청만 허용
        if current_user_id != user_id and current_user_role != 'admin':
            return jsonify({"error": "Permission denied"}), 403

        # 사용자 정보 조회
        user = User.get_user_by_id(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@user_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """
    ---
    tags:
      - Users
    summary: "Update User Information"
    description: "Allows the user to update their information. Admins can update any user's information."
    parameters:
      - in: path
        name: user_id
        required: true
        schema:
          type: integer
        description: "The ID of the user to update."
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              password:
                type: string
                description: "New password for the user."
              role:
                type: string
                enum: ["admin", "employer", "applicant"]
                description: "New role for the user (Admins only)."
    responses:
      200:
        description: "User updated successfully."
      400:
        description: "Validation error."
      403:
        description: "Permission denied."
      500:
        description: "Internal server error."
    """
    try:
        current_user_id = request.user['id']
        current_role = request.user['role']

        # 관리자 권한이 아닌 경우, 자기 자신의 정보만 수정 가능
        if current_role != 'admin' and current_user_id != user_id:
            return jsonify({"error": "Permission denied"}), 403

        data = request.json
        password = data.get('password')
        new_role = data.get('role')

        # 역할 변경은 관리자만 가능
        if new_role and current_role != 'admin':
            return jsonify({"error": "Permission denied to change role"}), 403

        # 비밀번호 유효성 검증
        if password and len(password) < 8:
            return jsonify({"error": "Password must be at least 8 characters long"}), 400

        update_fields = {}
        if password:
            update_fields['password'] = User.encode_password(password)
        if new_role:
            update_fields['role'] = new_role

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        result = User.update_user(user_id, update_fields)
        if "error" in result:
            return jsonify(result), 400

        return jsonify({"message": "User profile updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@user_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """
    ---
    tags:
      - Users
    summary: "Delete User"
    description: "Allows a user to delete their account. Admins can delete any user's account."
    parameters:
      - in: path
        name: user_id
        required: true
        schema:
          type: integer
        description: "The ID of the user to delete."
    responses:
      200:
        description: "User account deleted successfully."
      403:
        description: "Permission denied."
      404:
        description: "User not found."
      500:
        description: "Internal server error."
    """
    try:
        current_user_id = request.user['id']
        current_user_role = request.user['role']

        # 관리자 권한이 없는 사용자는 자신의 계정만 삭제 가능
        if current_user_id != user_id and current_user_role != 'admin':
            return jsonify({"error": "Permission denied"}), 403

        # 삭제 대상 사용자 검증
        user_to_delete = User.get_user_by_id(user_id)
        if not user_to_delete:
            return jsonify({"error": "User not found"}), 404

        # 사용자 삭제
        result = User.delete_user(user_id)
        if "error" in result:
            return jsonify(result), 400

        return jsonify({"message": "User account deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@user_bp.route('/<int:user_id>/bookmarks', methods=['POST'])
@jwt_required()
def toggle_bookmark(user_id):
    """
    ---
    tags:
      - User Bookmarks
    summary: "Toggle Bookmark"
    description: "Adds or removes a bookmark for a job posting."
    parameters:
      - in: path
        name: user_id
        required: true
        schema:
          type: integer
        description: "The ID of the user."
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              job_id:
                type: integer
                description: "The ID of the job to bookmark."
    responses:
      200:
        description: "Bookmark toggled successfully."
      400:
        description: "Validation error."
      403:
        description: "Permission denied."
    """
    if user_id != request.user['id']:
        return jsonify({"error": "Permission denied"}), 403

    data = request.json
    job_id = data.get('job_id')

    if not job_id:
        return jsonify({"error": "job_id is required"}), 400

    result = User.toggle_bookmark(user_id, job_id)
    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 200

@user_bp.route('/<int:user_id>/bookmarks', methods=['GET'])
@jwt_required()
def list_bookmarks(user_id):
    """
    ---
    tags:
      - User Bookmarks
    summary: "List Bookmarks"
    description: "Retrieves the list of bookmarked job postings for a user."
    parameters:
      - in: path
        name: user_id
        required: true
        schema:
          type: integer
        description: "The ID of the user."
    responses:
      200:
        description: "Bookmarks retrieved successfully."
      403:
        description: "Permission denied."
    """
    if user_id != request.user['id']:
        return jsonify({"error": "Permission denied"}), 403

    bookmarks = User.get_bookmarks(user_id)
    return jsonify(bookmarks), 200

@user_bp.route('/<int:user_id>/applications', methods=['POST'])
@jwt_required()
def add_application(user_id):
    """
    ---
    tags:
      - User Applications
    summary: "Add Application"
    description: "Adds a new job application for a user."
    parameters:
      - in: path
        name: user_id
        required: true
        schema:
          type: integer
        description: "The ID of the user."
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              job_id:
                type: integer
                description: "The ID of the job to apply for."
              content:
                type: string
                description: "Content of the application."
    responses:
      201:
        description: "Application added successfully."
      400:
        description: "Validation error."
      403:
        description: "Permission denied."
    """
    if user_id != request.user['id']:
        return jsonify({"error": "Permission denied"}), 403

    data = request.json
    job_id = data.get('job_id')
    content = data.get('content')

    if not job_id:
        return jsonify({"error": "job_id is required"}), 400

    if not content or content.strip() == "":
        return jsonify({"error": "content is required"}), 400

    result = User.add_application(user_id, job_id, content)
    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 201

@user_bp.route('/<int:user_id>/applications', methods=['GET'])
@jwt_required()
def list_applications(user_id):
    """
    ---
    tags:
      - User Applications
    summary: "List Applications"
    description: "Retrieves the list of job applications for a user."
    parameters:
      - in: path
        name: user_id
        required: true
        schema:
          type: integer
        description: "The ID of the user."
    responses:
      200:
        description: "Applications retrieved successfully."
      403:
        description: "Permission denied."
    """
    if user_id != request.user['id']:
        return jsonify({"error": "Permission denied"}), 403

    applications = User.get_applications(user_id)
    return jsonify(applications), 200

@user_bp.route('/<int:user_id>/applications/<int:job_id>', methods=['DELETE'])
@jwt_required()
def delete_application(user_id, job_id):
    """
    ---
    tags:
      - User Applications
    summary: "Delete Application"
    description: "Deletes a job application for a user."
    parameters:
      - in: path
        name: user_id
        required: true
        schema:
          type: integer
        description: "The ID of the user."
      - in: path
        name: job_id
        required: true
        schema:
          type: integer
        description: "The ID of the job application to delete."
    responses:
      200:
        description: "Application deleted successfully."
      403:
        description: "Permission denied."
    """
    if user_id != request.user['id']:
        return jsonify({"error": "Permission denied"}), 403

    result = User.delete_application(user_id, job_id)
    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 200
