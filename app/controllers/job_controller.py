from flask import Blueprint, jsonify, request
from app.services.job_service import get_all_jobs, create_job

# Blueprint: API 엔드포인트 그룹화
job_bp = Blueprint('job', __name__, url_prefix='/api/jobs')

@job_bp.route('/', methods=['GET'])
def list_jobs():
    """
    모든 공고를 조회.
    - GET /api/jobs 요청을 처리
    - Service 계층 호출 후 결과 반환
    """
    jobs = get_all_jobs()
    return jsonify(jobs), 200

@job_bp.route('/', methods=['POST'])
def add_job():
    """
    새로운 공고를 생성.
    - POST /api/jobs 요청을 처리
    - 요청 데이터(JSON) 검증 및 저장 후 결과 반환
    """
    data = request.json
    new_job = create_job(data)
    return jsonify(new_job), 201
