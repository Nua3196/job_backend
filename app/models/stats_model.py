from app.utils.db import get_db

class Stats:
    @staticmethod
    def get_company_job_count():
        """
        회사별 공고 수 통계
        Returns:
            list: 회사 이름, 공고 수, 전체 대비 비율
        """
        db = get_db()
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT 
                    company.name AS company_name,
                    COUNT(job.id) AS job_count,
                    ROUND((COUNT(job.id) / (SELECT COUNT(*) FROM job)) * 100, 2) AS percentage
                FROM company
                LEFT JOIN job ON company.id = job.company
                GROUP BY company.name
                ORDER BY job_count DESC
            """)
            return cursor.fetchall()
        finally:
            cursor.close()

    @staticmethod
    def get_tech_job_count():
        """
        기술별 공고 수 통계
        Returns:
            list: 기술 이름, 공고 수, 전체 대비 비율
        """
        db = get_db()
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT 
                    tech.name AS tech_name,
                    COUNT(job_tech.job) AS job_count,
                    ROUND((COUNT(job_tech.job) / (SELECT COUNT(*) FROM job)) * 100, 2) AS percentage
                FROM tech
                LEFT JOIN job_tech ON tech.id = job_tech.tech
                GROUP BY tech.name
                ORDER BY job_count DESC
            """)
            return cursor.fetchall()
        finally:
            cursor.close()

    @staticmethod
    def get_job_application_count():
        """
        공고별 지원 수 통계
        Returns:
            list: 공고 제목, 지원 수, 전체 지원 대비 비율
        """
        db = get_db()
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT 
                    job.title AS job_title,
                    COUNT(application.user) AS application_count,
                    ROUND((COUNT(application.user) / (SELECT COUNT(*) FROM application)) * 100, 2) AS percentage
                FROM job
                LEFT JOIN application ON job.id = application.job
                GROUP BY job.title
                ORDER BY application_count DESC
            """)
            return cursor.fetchall()
        finally:
            cursor.close()