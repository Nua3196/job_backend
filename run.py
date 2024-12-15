from app import create_app

# Flask 애플리케이션 초기화
app = create_app()

if __name__ == "__main__":
    """
    애플리케이션 실행.
    - 개발 환경에서는 debug=True로 실행
    """
    app.run(debug=True)
