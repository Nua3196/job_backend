import os
import logging
from app import create_app

# Flask 애플리케이션 초기화
app = create_app()

if __name__ == "__main__":
    """
    애플리케이션 실행.
    - 환경 변수 FLASK_ENV, FLASK_HOST, FLASK_PORT 사용
    - 기본값: development 환경, localhost:5000
    """
    # 환경 변수에서 실행 환경, 호스트, 포트 가져오기
    env = os.getenv('FLASK_ENV', 'development')
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))

    # 로깅 설정
    logging.basicConfig(level=logging.DEBUG if env == 'development' else logging.INFO)

    # 애플리케이션 실행
    app.run(debug=(env == 'development'), host=host, port=port)
