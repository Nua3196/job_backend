from app.utils.db import get_db

def get_jobs_from_db():
    """
    데이터베이스에서 모든 공고를 조회.
    - SELECT 쿼리 실행
    - 결과 반환
    """
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM job")
    return cursor.fetchall()

def add_job_to_db(data):
    """
    새로운 공고를 데이터베이스에 추가.
    - INSERT 쿼리 실행
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO job (company, creator, title, link, career_condition, education, deadline, job_sector) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (
            data['company'], data['creator'], data['title'], data['link'],
            data['career_condition'], data['education'], data['deadline'], data['job_sector']
        )
    )
    db.commit()
