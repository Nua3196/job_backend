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
    def get_all_sorted(page, size, sort_by, order):
        """
        공고 목록 정렬 및 페이지네이션
        Args:
            page (int): 페이지 번호
            size (int): 페이지 크기
            sort_by (str): 정렬 기준 필드
            order (str): 정렬 순서 ('asc', 'desc')
        Returns:
            list: 정렬된 공고 목록
        """
        db = get_db()
        cursor = db.cursor(dictionary=True)
        try:
            offset = (page - 1) * size

            # 정렬 기준 및 순서 검증
            valid_fields = {'id', 'title', 'deadline', 'job_sector'}
            if sort_by not in valid_fields:
                sort_by = 'id'  # 기본값

            query = f"""
                SELECT * FROM job
                ORDER BY {sort_by} {order}
                LIMIT %s OFFSET %s
            """
            cursor.execute(query, (size, offset))
            return cursor.fetchall()
        finally:
            cursor.close()

    @staticmethod
    def get_paginated(page, size):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        try:
            offset = (page - 1) * size
            cursor.execute("SELECT * FROM job LIMIT %s OFFSET %s", (size, offset))
            return cursor.fetchall()
        finally:
            cursor.close()

    @staticmethod
    def get_total_count():
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM job")
            return cursor.fetchone()[0]
        finally:
            cursor.close()

    @staticmethod
    def update(job_id, fields):
        db = get_db()
        cursor = db.cursor()
        try:
            # 공고 데이터 업데이트
            set_clause = ", ".join(f"{key} = %s" for key in fields.keys() if key not in ['tech_ids', 'location_ids'])
            values = [fields[key] for key in fields.keys() if key not in ['tech_ids', 'location_ids']] + [job_id]
            if set_clause:
                cursor.execute(f"UPDATE job SET {set_clause} WHERE id = %s", values)

            # 기술 및 위치 데이터 업데이트
            if 'tech_ids' in fields:
                cursor.execute("DELETE FROM job_tech WHERE job = %s", (job_id,))
                for tech_id in fields['tech_ids']:
                    cursor.execute("INSERT INTO job_tech (job, tech) VALUES (%s, %s)", (job_id, tech_id))

            if 'location_ids' in fields:
                cursor.execute("DELETE FROM job_location WHERE job = %s", (job_id,))
                for location_id in fields['location_ids']:
                    cursor.execute("INSERT INTO job_location (job, location) VALUES (%s, %s)", (job_id, location_id))

            db.commit()
            return {"message": "Job updated successfully"}
        finally:
            cursor.close()


    @staticmethod
    def create(data):
        db = get_db()
        cursor = db.cursor()
        try:
            # 공고 데이터 추가
            cursor.execute(
                "INSERT INTO job (company, creator, title, link, career_condition, education, deadline, job_sector) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    data['company'], data['creator'], data['title'], data['link'],
                    data['career_condition'], data['education'], data['deadline'], data['job_sector']
                )
            )
            job_id = cursor.lastrowid

            # 기술 및 위치 데이터 추가
            for tech_id in data.get('tech_ids', []):
                cursor.execute("INSERT INTO job_tech (job, tech) VALUES (%s, %s)", (job_id, tech_id))

            for location_id in data.get('location_ids', []):
                cursor.execute("INSERT INTO job_location (job, location) VALUES (%s, %s)", (job_id, location_id))

            db.commit()
            return {"message": "Job created successfully"}
        finally:
            cursor.close()

    @staticmethod
    def delete(job_id):
        db = get_db()
        cursor = db.cursor()
        try:
            # 공고 삭제 (관계 데이터는 ON DELETE CASCADE로 자동 처리)
            cursor.execute("DELETE FROM job WHERE id = %s", (job_id,))
            db.commit()
            return {"message": "Job deleted successfully"}
        finally:
            cursor.close()

    @staticmethod
    def search_and_filter(filters):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        try:
            query = "SELECT * FROM job"
            conditions = []
            values = []

            if filters.get('keyword'):
                conditions.append("(title LIKE %s OR company LIKE %s)")
                keyword = f"%{filters['keyword']}%"
                values.extend([keyword, keyword])

            if filters.get('location'):
                conditions.append("id IN (SELECT job FROM job_location WHERE location = %s)")
                values.append(filters['location'])

            if filters.get('tech'):
                conditions.append("id IN (SELECT job FROM job_tech WHERE tech = %s)")
                values.append(filters['tech'])

            if filters.get('career_condition'):
                conditions.append("career_condition = %s")
                values.append(filters['career_condition'])

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            cursor.execute(query, values)
            return cursor.fetchall()
        finally:
            cursor.close()

    @staticmethod
    def validate_company(company_id):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM company WHERE id = %s", (company_id,))
            return cursor.fetchone()[0] > 0
        finally:
            cursor.close()

    @staticmethod
    def validate_creator(creator_id):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM user WHERE id = %s", (creator_id,))
            return cursor.fetchone()[0] > 0
        finally:
            cursor.close()

    @staticmethod
    def is_duplicate_link(link):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM job WHERE link = %s", (link,))
            return cursor.fetchone()[0] > 0
        finally:
            cursor.close()

    @staticmethod
    def get_details(job_id):
        """
        특정 공고의 세부 정보를 반환
        Args:
            job_id (int): 조회할 공고 ID
        Returns:
            dict: 공고 세부 정보
        """
        db = get_db()
        cursor = db.cursor(dictionary=True)
        try:
            # 기본 공고 정보 조회
            cursor.execute("SELECT * FROM job WHERE id = %s", (job_id,))
            job = cursor.fetchone()
            if not job:
                return None

            # 기술 스택 정보 조회
            cursor.execute("""
                SELECT tech.id, tech.name 
                FROM tech 
                JOIN job_tech ON tech.id = job_tech.tech 
                WHERE job_tech.job = %s
            """, (job_id,))
            job['tech_stack'] = cursor.fetchall()

            # 위치 정보 조회
            cursor.execute("""
                SELECT location.id, location.name 
                FROM location 
                JOIN job_location ON location.id = job_location.location 
                WHERE job_location.job = %s
            """, (job_id,))
            job['locations'] = cursor.fetchall()

            return job
        finally:
            cursor.close()

    @staticmethod
    def get_creator_id(job_id):
        """
        특정 공고의 작성자 ID를 반환
        Args:
            job_id (int): 공고 ID
        Returns:
            int: 작성자 ID 또는 None
        """
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT creator FROM job WHERE id = %s", (job_id,))
            result = cursor.fetchone()
            return result[0] if result else None
        finally:
            cursor.close()
