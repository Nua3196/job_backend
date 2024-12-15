from flask import Flask
from app.controllers import job_controller, auth_controller

def create_app():
    """
    Flask 애플리케이션을 생성 및 초기화.
    - 환경 설정 로드
    - 블루프린트 등록
    """
    app = Flask(__name__)

    # 환경 설정 파일 로드
    app.config.from_pyfile('../config.py')

    # 블루프린트 등록: 각 모듈별 라우팅 정의 연결
    app.register_blueprint(job_controller.job_bp)
    app.register_blueprint(auth_controller.auth_bp)

    return app
