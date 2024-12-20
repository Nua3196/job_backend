from flask import Blueprint, jsonify, request
from app.models.job_model import Job

# Blueprint: API 엔드포인트 그룹화
job_bp = Blueprint('job', __name__, url_prefix='/api/jobs')

@job_bp.route('/', methods=['GET'])
def list_jobs():
    """
    공고 목록 조회 (정렬 및 페이지네이션 지원)
    - 기본 정렬 기준: id DESC (최신 공고 순)
    """
    try:
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 20))
        sort_by = request.args.get('sort_by', 'id')  # 기본 정렬 기준
        order = request.args.get('order', 'desc')

        if order not in ['asc', 'desc']:
            return jsonify({"error": "Invalid order parameter"}), 400

        jobs = Job.get_all_sorted(page, size, sort_by, order)
        total_count = Job.get_total_count()

        return jsonify({
            "data": jobs,
            "pagination": {
                "current_page": page,
                "page_size": size,
                "total_items": total_count,
                "total_pages": (total_count + size - 1) // size
            }
        }), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

from app.middlewares.auth import jwt_required

@job_bp.route('/', methods=['POST'])
@jwt_required(required_roles=['admin', 'employer'])
def add_job():
    """
    새로운 공고를 생성.
    - 요청 데이터(JSON): title, company, creator, career_condition, education, deadline, job_sector
    """
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid input"}), 400

        # 필수 필드 검증
        required_fields = ["title", "company", "creator"]
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"'{field}' is required"}), 400

        # 회사 및 생성자 유효성 확인 (Optional)
        if not Job.validate_company(data["company"]):
            return jsonify({"error": f"Invalid company ID: {data['company']}"}), 400

        if not Job.validate_creator(data["creator"]):
            return jsonify({"error": f"Invalid creator ID: {data['creator']}"}), 400

        # 중복 링크 확인
        if Job.is_duplicate_link(data["link"]):
            return jsonify({"error": f"Duplicate job link: {data['link']}"}), 400

        # 공고 생성
        result = Job.create(data)
        return jsonify(result), 201

    except Exception as e:
        return jsonify({"error": f"Failed to create job: {str(e)}"}), 500


@job_bp.route('/<int:job_id>', methods=['PUT'])
@jwt_required(required_roles=['admin', 'employer'])
def update_job(job_id):
    """
    채용 공고 수정 API
    - 요청 데이터(JSON): title, company, creator, career_condition, education, deadline, job_sector
    """
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid input"}), 400

        # 수정 가능한 필드
        updatable_fields = {
            "title", "company", "creator", "career_condition",
            "education", "deadline", "job_sector"
        }
        update_data = {key: value for key, value in data.items() if key in updatable_fields}

        if not update_data:
            return jsonify({"error": "No valid fields to update"}), 400

        # 업데이트 수행
        result = Job.update(job_id, update_data)
        if "error" in result:
            return jsonify(result), 400

        return jsonify({"message": "Job updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@job_bp.route('/<int:job_id>', methods=['DELETE'])
@jwt_required(required_roles=['admin', 'employer'])
def delete_job(job_id):
    """
    채용 공고 삭제 API
    - 경로 매개변수: job_id
    - 성공 시 삭제 완료 메시지 반환
    """
    try:
        # 공고 삭제 수행
        result = Job.delete(job_id)
        if "error" in result:
            return jsonify(result), 400

        return jsonify({"message": "Job deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@job_bp.route('/search', methods=['GET'])
def search_jobs():
    """
    공고 검색 및 필터링 API
    - 쿼리 매개변수: keyword, location, tech, career_condition
    """
    try:
        # 쿼리 매개변수 가져오기
        keyword = request.args.get('keyword', '').strip()
        location = request.args.get('location')
        tech = request.args.get('tech')
        career_condition = request.args.get('career_condition')

        # 검색 및 필터링 수행
        filters = {
            "keyword": keyword,
            "location": location,
            "tech": tech,
            "career_condition": career_condition
        }
        results = Job.search_and_filter(filters)

        return jsonify(results), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@job_bp.route('/<int:job_id>', methods=['GET'])
def get_job_details(job_id):
    """
    공고 상세 조회 API
    - 경로 매개변수: job_id
    """
    try:
        # 공고 상세 정보 조회
        job_details = Job.get_details(job_id)
        if not job_details:
            return jsonify({"error": "Job not found"}), 404

        return jsonify(job_details), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
