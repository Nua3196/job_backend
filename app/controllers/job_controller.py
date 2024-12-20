from flask import Blueprint, jsonify, request
from app.models.job_model import Job
from app.utils.jwt_handler import decode_token

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
    새로운 공고를 생성
    - 요청 데이터(JSON): title, link, career_condition, education, deadline, job_sector
    """
    try:
        # JWT 토큰에서 사용자 정보 추출
        auth_header = request.headers.get('Authorization')
        token = auth_header.split(" ")[1]
        decoded_token = decode_token(token)

        user_id = decoded_token.get('id')
        role = decoded_token.get('role')
        company_id = None

        # 역할에 따라 company 설정
        if role == 'admin':
            # admin은 JSON에서 company 정보를 받음
            company_id = request.json.get('company')
            if not company_id:
                return jsonify({"error": "Company ID is required for admin users"}), 400

            # company 유효성 검증
            if not Job.validate_company(company_id):
                return jsonify({"error": f"Invalid company ID: {company_id}"}), 400

        elif role == 'employer':
            # employer는 JWT에서 company 정보를 가져옴
            company_id = decoded_token.get('company')
            if not company_id:
                return jsonify({"error": "No company associated with the employer"}), 400

        # 요청 데이터 검증
        data = request.json
        if not data:
            return jsonify({"error": "Invalid input"}), 400

        required_fields = ["title", "link", "career_condition", "education", "deadline", "job_sector"]
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"'{field}' is required"}), 400

        # 중복 링크 확인
        if Job.is_duplicate_link(data["link"]):
            return jsonify({"error": f"Duplicate job link: {data['link']}"}), 400

        # 공고 데이터 생성
        job_data = {
            "creator": user_id,  # creator는 사용자 ID
            "company": company_id,
            "title": data["title"],
            "link": data["link"],
            "career_condition": data["career_condition"],
            "education": data["education"],
            "deadline": data["deadline"],
            "job_sector": data["job_sector"]
        }

        # 공고 생성
        result = Job.create(job_data)
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
