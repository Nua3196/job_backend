import logging
from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
import time
from app.controllers import (
    auth_controller,
    job_controller,
    company_controller,
    user_controller,
    stats_controller
)

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    # 블루프린트 등록
    app.register_blueprint(auth_controller.auth_bp)  # 인증
    app.register_blueprint(job_controller.job_bp)  # 채용 공고
    app.register_blueprint(company_controller.company_bp)  # 회사 정보
    app.register_blueprint(user_controller.user_bp)  # 사용자 (북마크 및 지원 내역 포함)
    app.register_blueprint(stats_controller.stats_bp)  # 통계

    # Swagger UI 설정
    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.yaml'  # YAML 파일 경로
    swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # 로깅 설정
    logging.basicConfig(
        level=logging.DEBUG if app.config.get("DEBUG") else logging.WARNING,
        format='%(asctime)s %(levelname)s: %(message)s',
        handlers=[
            logging.FileHandler("app.log"),  # 파일 로깅
            logging.StreamHandler()  # 콘솔 출력
        ]
    )
    app.logger = logging.getLogger()

    # 요청 및 응답 로깅
    @app.before_request
    def log_request_info():
        request.start_time = time.time()
        app.logger.info(f"Request: {request.method} {request.url}")

    @app.after_request
    def log_response_info(response):
        duration = time.time() - request.start_time
        app.logger.info(f"Response: {request.method} {request.url} - {response.status} ({duration:.3f}s)")
        return response

    # 전역 에러 처리기
    @app.errorhandler(400)
    def bad_request_error(error):
        return jsonify({"error": "Bad Request", "message": str(error)}), 400

    @app.errorhandler(401)
    def unauthorized_error(error):
        return jsonify({"error": "Unauthorized", "message": str(error)}), 401

    @app.errorhandler(403)
    def forbidden_error(error):
        return jsonify({"error": "Forbidden", "message": str(error)}), 403

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"error": "Not Found", "message": str(error)}), 404

    @app.errorhandler(Exception)
    def internal_server_error(error):
        app.logger.error(f"Unexpected error: {str(error)}")
        return jsonify({"error": "Internal Server Error", "message": "An unexpected error occurred"}), 500

    return app
