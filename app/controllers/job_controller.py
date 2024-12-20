from flask import Blueprint, jsonify, request
from app.models.job_model import Job

# Blueprint: API 엔드포인트 그룹화
job_bp = Blueprint('job', __name__, url_prefix='/api/jobs')

@job_bp.route('/', methods=['GET'])
def list_jobs():
    """
    모든 공고를 조회.
    - GET /api/jobs 요청을 처리
    """
    try:
        jobs = Job.get_all()  # Job 모델의 get_all 메서드 호출
        return jsonify(jobs), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch jobs: {str(e)}"}), 500

@job_bp.route('/', methods=['POST'])
def add_job():
    """
    새로운 공고를 생성.
    - POST /api/jobs 요청을 처리
    """
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid input"}), 400
        result = Job.create(data)  # Job 모델의 create 메서드 호출
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": f"Failed to create job: {str(e)}"}), 500
