from flask import Blueprint, jsonify
from app.models.stats_model import Stats

stats_bp = Blueprint('stats', __name__, url_prefix='/api/stats')

@stats_bp.route('/companies', methods=['GET'])
def company_stats():
    """
    ---
    tags:
      - Statistics
    summary: "Company Statistics"
    description: "Retrieves the number of job postings for each company."
    responses:
      200:
        description: "Company statistics retrieved successfully."
      500:
        description: "Internal server error."
    """
    try:
        stats = Stats.get_company_job_count()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@stats_bp.route('/techs', methods=['GET'])
def tech_stats():
    """
    ---
    tags:
      - Statistics
    summary: "Technology Statistics"
    description: "Retrieves the number of job postings for each technology."
    responses:
      200:
        description: "Technology statistics retrieved successfully."
      500:
        description: "Internal server error."
    """
    try:
        stats = Stats.get_tech_job_count()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@stats_bp.route('/jobs', methods=['GET'])
def job_application_stats():
    """
    ---
    tags:
      - Statistics
    summary: "Job Application Statistics"
    description: "Retrieves the number of applications for each job posting."
    responses:
      200:
        description: "Job application statistics retrieved successfully."
      500:
        description: "Internal server error."
    """
    try:
        stats = Stats.get_job_application_count()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500