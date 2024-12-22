from app.utils.db import get_db

class Application:
    @staticmethod
    def add(user_id, job_id, content):
        """
        지원 내역 추가
        Args:
            user_id (int): 사용자 ID
            job_id (int): 공고 ID
            content (str): 지원 내용
        Returns:
            dict: 성공 메시지 또는 에러 메시지
        """
        db = get_db()
        cursor = db.cursor()
        try:
            # 중복 지원 방지
            cursor.execute("SELECT 1 FROM application WHERE user = %s AND job = %s", (user_id, job_id))
            if cursor.fetchone():
                return {"error": "Already applied for this job"}

            # 지원 내역 추가
            cursor.execute(
                "INSERT INTO application (user, job, content) VALUES (%s, %s, %s)",
                (user_id, job_id, content)
            )
            db.commit()
            return {"message": "Application added"}
        except Exception as e:
            return {"error": f"Failed to add application: {str(e)}"}
        finally:
            cursor.close()

    @staticmethod
    def get_by_user(user_id):
        """
        특정 사용자의 지원 내역 조회
        Args:
            user_id (int): 사용자 ID
        Returns:
            list: 지원 내역 목록
        """
        db = get_db()
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT job.*, a.content FROM job
                JOIN application a ON job.id = a.job
                WHERE a.user = %s
            """, (user_id,))
            return cursor.fetchall()
        finally:
            cursor.close()

    @staticmethod
    def delete(user_id, job_id):
        """
        지원 내역 삭제
        Args:
            user_id (int): 사용자 ID
            job_id (int): 공고 ID
        Returns:
            dict: 성공 메시지 또는 에러 메시지
        """
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("DELETE FROM application WHERE user = %s AND job = %s", (user_id, job_id))
            db.commit()
            return {"message": "Application deleted"}
        except Exception as e:
            return {"error": f"Failed to delete application: {str(e)}"}
        finally:
            cursor.close()

    @staticmethod
    def get_applications_by_job(job_id):
        """
        특정 공고에 대한 지원 목록 조회
        Args:
            job_id (int): 공고 ID
        Returns:
            list: 지원 정보 리스트
        """
        db = get_db()
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT a.user, u.email, u.role, a.content, a.created_at
                FROM application a
                JOIN user u ON a.user = u.id
                WHERE a.job = %s
            """, (job_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
