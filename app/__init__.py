from flask import Flask
from app.controllers import job_controller, auth_controller

def create_app():
    app = Flask(__name__)

    # 환경설정 로드
    app.config.from_pyfile('../config.py')

    # 블루프린트 등록
    app.register_blueprint(job_controller.job_bp)
    app.register_blueprint(auth_controller.auth_bp)

    return app
