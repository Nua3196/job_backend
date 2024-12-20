from flask import Blueprint, jsonify, request
from app.models.user_model import User
from app.middlewares.auth import jwt_required

user_bp = Blueprint('user', __name__, url_prefix='/api/users')

@user_bp.route('/<int:user_id>/bookmarks', methods=['POST'])
@jwt_required()
def toggle_bookmark(user_id):
    """
    북마크 추가/제거 API
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
    북마크 목록 조회 API
    """
    if user_id != request.user['id']:
        return jsonify({"error": "Permission denied"}), 403

    bookmarks = User.get_bookmarks(user_id)
    return jsonify(bookmarks), 200

@user_bp.route('/<int:user_id>/applications', methods=['POST'])
@jwt_required()
def add_application(user_id):
    """
    지원하기 API
    """
    if user_id != request.user['id']:
        return jsonify({"error": "Permission denied"}), 403

    data = request.json
    job_id = data.get('job_id')

    if not job_id:
        return jsonify({"error": "job_id is required"}), 400

    result = User.add_application(user_id, job_id)
    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 201

@user_bp.route('/<int:user_id>/applications', methods=['GET'])
@jwt_required()
def list_applications(user_id):
    """
    지원 내역 조회 API
    """
    if user_id != request.user['id']:
        return jsonify({"error": "Permission denied"}), 403

    applications = User.get_applications(user_id)
    return jsonify(applications), 200

@user_bp.route('/<int:user_id>/applications/<int:job_id>', methods=['DELETE'])
@jwt_required()
def delete_application(user_id, job_id):
    """
    지원 취소 API
    """
    if user_id != request.user['id']:
        return jsonify({"error": "Permission denied"}), 403

    result = User.delete_application(user_id, job_id)
    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 200
