from app.models.job_model import get_jobs_from_db, add_job_to_db

def get_all_jobs():
    """
    모든 공고를 조회하는 비즈니스 로직.
    - Model 계층 호출
    """
    return get_jobs_from_db()

def create_job(data):
    """
    새로운 공고를 생성하는 비즈니스 로직.
    - 요청 데이터를 Model 계층에 전달
    - 성공 메시지 반환
    """
    add_job_to_db(data)
    return {"message": "Job created successfully"}
