from app.utils.db import get_db

class Job:
    def __init__(self, company, creator, title, link, career_condition, education, deadline, job_sector):
        self.company = company
        self.creator = creator
        self.title = title
        self.link = link
        self.career_condition = career_condition
        self.education = education
        self.deadline = deadline
        self.job_sector = job_sector

    @staticmethod
    def get_all():
        """
        데이터베이스에서 모든 공고를 조회.
        Returns:
            list: 공고 데이터 리스트
        """
        db = get_db()
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM job")
            return cursor.fetchall()
        finally:
            cursor.close()

    @staticmethod
    def create(data):
        """
        새로운 공고를 데이터베이스에 추가.
        Args:
            data (dict): 새로운 공고 정보
        Returns:
            dict: 성공 메시지
        """
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                "INSERT INTO job (company, creator, title, link, career_condition, education, deadline, job_sector) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    data['company'], data['creator'], data['title'], data['link'],
                    data['career_condition'], data['education'], data['deadline'], data['job_sector']
                )
            )
            db.commit()
            return {"message": "Job created successfully"}
        finally:
            cursor.close()

class Tech:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Location:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class JobTech:
    def __init__(self, job, tech):
        self.job = job
        self.tech = tech

class JobLocation:
    def __init__(self, job, location):
        self.job = job
        self.location = location
