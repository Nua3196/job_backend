from flask import Blueprint, jsonify, request
from app.models.job_model import Job
from app.middlewares.auth import jwt_required

# Blueprint: API 엔드포인트 그룹화
job_bp = Blueprint('job', __name__, url_prefix='/api/jobs')

@job_bp.route('/', methods=['GET'])
def list_jobs():
    """
    ---
    tags:
      - Jobs
    summary: "List Jobs"
    description: "Retrieve a list of jobs with pagination and sorting."
    parameters:
      - in: query
        name: page
        schema:
          type: integer
          default: 1
        description: "Page number."
      - in: query
        name: size
        schema:
          type: integer
          default: 20
        description: "Number of items per page."
      - in: query
        name: sort_by
        schema:
          type: string
          default: "id"
        description: "Field to sort by."
      - in: query
        name: order
        schema:
          type: string
          enum: [asc, desc]
          default: "desc"
        description: "Sort order."
    responses:
      200:
        description: "List of jobs retrieved successfully."
      500:
        description: "Internal server error."
    """
    try:
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 20))
        sort_by = request.args.get('sort_by', 'id')
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

@job_bp.route('/', methods=['POST'])
@jwt_required(required_roles=['admin', 'employer'])
def add_job():
    """
    ---
    tags:
      - Jobs
    summary: "Add a Job"
    description: "Create a new job posting."
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              title:
                type: string
                description: "Title of the job."
              link:
                type: string
                description: "Link to the job posting."
              career_condition:
                type: string
                description: "Career condition required for the job."
              education:
                type: string
                description: "Education level required for the job."
              deadline:
                type: string
                description: "Application deadline for the job."
              job_sector:
                type: string
                description: "Sector of the job."
              company:
                type: integer
                description: "Company ID (required for admin users)."
              tech_ids:
                type: array
                items:
                  type: integer
                description: "List of technology IDs."
              location_ids:
                type: array
                items:
                  type: integer
                description: "List of location IDs."
    responses:
      201:
        description: "Job created successfully."
      400:
        description: "Validation error."
      500:
        description: "Internal server error."
    """
    try:
        user_id = request.user['id']
        role = request.user['role']
        company_id = None

        if role == 'admin':
            company_id = request.json.get('company')
            if not company_id:
                return jsonify({"error": "Company ID is required for admin users"}), 400

            if not Job.validate_company(company_id):
                return jsonify({"error": f"Invalid company ID: {company_id}"}), 400

        elif role == 'employer':
            company_id = request.user.get('company')
            if not company_id:
                return jsonify({"error": "No company associated with the employer"}), 400

        data = request.json
        if not data:
            return jsonify({"error": "Invalid input"}), 400

        required_fields = ["title", "link", "career_condition", "education", "deadline", "job_sector"]
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"'{field}' is required"}), 400

        if Job.is_duplicate_link(data["link"]):
            return jsonify({"error": f"Duplicate job link: {data['link']}"}), 400

        tech_ids = data.get("tech_ids", [])
        location_ids = data.get("location_ids", [])

        # 공고 생성
        job_data = {
            "creator": user_id,
            "company": company_id,
            "title": data["title"],
            "link": data["link"],
            "career_condition": data["career_condition"],
            "education": data["education"],
            "deadline": data["deadline"],
            "job_sector": data["job_sector"],
            "tech_ids": tech_ids,
            "location_ids": location_ids,
        }

        result = Job.create(job_data)
        return jsonify(result), 201

    except Exception as e:
        return jsonify({"error": f"Failed to create job: {str(e)}"}), 500

@job_bp.route('/<int:job_id>', methods=['PUT'])
@jwt_required(required_roles=['admin', 'employer'])
def update_job(job_id):
    """
    ---
    tags:
      - Jobs
    summary: "Update Job"
    description: "Updates an existing job posting."
    parameters:
      - in: path
        name: job_id
        required: true
        schema:
          type: integer
        description: "The ID of the job to update."
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              title:
                type: string
              company:
                type: integer
              creator:
                type: integer
              career_condition:
                type: string
              education:
                type: string
              deadline:
                type: string
              job_sector:
                type: string
              tech_ids:
                type: array
                items:
                  type: integer
                description: "List of technology IDs."
              location_ids:
                type: array
                items:
                  type: integer
                description: "List of location IDs."
    responses:
      200:
        description: "Job updated successfully."
      400:
        description: "Validation error."
      500:
        description: "Internal server error."
    """
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid input"}), 400

        updatable_fields = {
            "title", "company", "creator", "career_condition",
            "education", "deadline", "job_sector", "tech_ids", "location_ids"
        }
        update_data = {key: value for key, value in data.items() if key in updatable_fields}

        if not update_data:
            return jsonify({"error": "No valid fields to update"}), 400

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
    ---
    tags:
      - Jobs
    summary: "Delete Job"
    description: "Deletes a job posting."
    parameters:
      - in: path
        name: job_id
        required: true
        schema:
          type: integer
        description: "The ID of the job to delete."
    responses:
      200:
        description: "Job deleted successfully."
      404:
        description: "Job not found."
      500:
        description: "Internal server error."
    """
    try:
        result = Job.delete(job_id)
        if "error" in result:
            return jsonify(result), 400

        return jsonify({"message": "Job deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@job_bp.route('/search', methods=['GET'])
def search_jobs():
    """
    ---
    tags:
      - Jobs
    summary: "Search Jobs"
    description: "Searches and filters job postings based on various criteria."
    parameters:
      - in: query
        name: keyword
        schema:
          type: string
        description: "Search keyword for job titles or descriptions."
      - in: query
        name: location
        schema:
          type: string
        description: "Location filter."
      - in: query
        name: tech
        schema:
          type: string
        description: "Technology filter."
      - in: query
        name: career_condition
        schema:
          type: string
        description: "Career condition filter."
    responses:
      200:
        description: "Search results returned successfully."
      500:
        description: "Internal server error."
    """
    try:
        keyword = request.args.get('keyword', '').strip()
        location = request.args.get('location')
        tech = request.args.get('tech')
        career_condition = request.args.get('career_condition')

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
    ---
    tags:
      - Jobs
    summary: "Get Job Details"
    description: "Retrieves detailed information for a specific job."
    parameters:
      - in: path
        name: job_id
        required: true
        schema:
          type: integer
        description: "The ID of the job to retrieve details for."
    responses:
      200:
        description: "Job details returned successfully."
      404:
        description: "Job not found."
      500:
        description: "Internal server error."
    """
    try:
        job_details = Job.get_details(job_id)
        if not job_details:
            return jsonify({"error": "Job not found"}), 404

        return jsonify(job_details), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

import logging

@job_bp.route('/<int:job_id>/applications', methods=['GET'])
@jwt_required()
def get_applications_by_job(job_id):
    """
    ---
    tags:
      - Job Applications
    summary: "List Applications for a Job"
    description: "Retrieves a list of applications for a specific job. Only accessible by the job creator."
    parameters:
      - in: path
        name: job_id
        required: true
        schema:
          type: integer
        description: "The ID of the job to retrieve applications for."
    responses:
      200:
        description: "List of applications retrieved successfully."
      403:
        description: "Permission denied."
      404:
        description: "Job not found or no applications."
      500:
        description: "Internal server error."
    """
    try:
        # 공고 작성자 확인
        job_creator_id = Job.get_creator_id(job_id)
        if not job_creator_id:
            return jsonify({"error": "Job not found"}), 404

        # 작성자 권한 검증
        if job_creator_id != request.user['id']:
            logging.warning(
                f"Unauthorized access attempt: User {request.user['id']} tried to access applications for Job {job_id}"
            )
            return jsonify({"error": "Permission denied"}), 403

        # 공고에 대한 지원 목록 조회
        applications = Application.get_applications_by_job(job_id)

        logging.info(f"User {request.user['id']} accessed applications for Job {job_id}")
        return jsonify(applications), 200
    except Exception as e:
        logging.error(f"Error while retrieving applications for Job {job_id}: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
