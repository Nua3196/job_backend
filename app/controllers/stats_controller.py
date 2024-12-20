from flask import Blueprint, jsonify
from app.models.stats_model import Stats

stats_bp = Blueprint('stats', __name__, url_prefix='/api/stats')

@stats_bp.route('/companies', methods=['GET'])
def company_stats():
    """
    회사별 공고 수 통계 API
    """
    try:
        stats = Stats.get_company_job_count()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@stats_bp.route('/techs', methods=['GET'])
def tech_stats():
    """
    기술별 공고 수 통계 API
    """
    try:
        stats = Stats.get_tech_job_count()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@stats_bp.route('/jobs', methods=['GET'])
def job_application_stats():
    """
    공고별 지원 수 통계 API
    """
    try:
        stats = Stats.get_job_application_count()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500