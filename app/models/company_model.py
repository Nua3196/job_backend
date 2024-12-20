from app.utils.db import get_db

class Company:
    @staticmethod
    def validate(company_id):
        """
        회사 ID가 유효한지 확인
        Args:
            company_id (int): 회사 ID
        Returns:
            bool: 회사 ID가 유효하면 True, 아니면 False
        """
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT id FROM company WHERE id = %s", (company_id,))
            return cursor.fetchone() is not None
        finally:
            cursor.close()

    @staticmethod
    def get_or_create(name, link):
        """
        회사 정보를 조회하거나 없으면 생성
        Args:
            name (str): 회사 이름
            link (str): 회사 링크
        Returns:
            int: 회사 ID
        """
        db = get_db()
        cursor = db.cursor(dictionary=True)
        try:
            # 기존 회사 정보 조회
            cursor.execute("SELECT id FROM company WHERE name = %s AND link = %s", (name, link))
            company = cursor.fetchone()

            if company:
                return company['id']  # 기존 회사 ID 반환

            # 회사 정보 추가
            cursor.execute(
                "INSERT INTO company (name, link) VALUES (%s, %s)",
                (name, link)
            )
            db.commit()
            return cursor.lastrowid  # 새로 생성된 회사 ID 반환
        except Exception as e:
            raise Exception(f"Failed to get or create company: {str(e)}")
        finally:
            cursor.close()

    @staticmethod
    def get_all():
        db = get_db()
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM company")
            return cursor.fetchall()
        finally:
            cursor.close()

    @staticmethod
    def get_by_id(company_id):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM company WHERE id = %s", (company_id,))
            return cursor.fetchone()
        finally:
            cursor.close()

    @staticmethod
    def create(data):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                "INSERT INTO company (name, link) VALUES (%s, %s)",
                (data['name'], data['link'])
            )
            db.commit()
            return {"message": "Company created successfully", "id": cursor.lastrowid}
        except Exception as e:
            return {"error": f"Failed to create company: {str(e)}"}
        finally:
            cursor.close()

    @staticmethod
    def update(company_id, data):
        db = get_db()
        cursor = db.cursor()
        try:
            set_clause = ", ".join(f"{key} = %s" for key in data.keys())
            values = list(data.values()) + [company_id]
            cursor.execute(f"UPDATE company SET {set_clause} WHERE id = %s", values)
            db.commit()
            return {"message": "Company updated successfully"}
        except Exception as e:
            return {"error": f"Failed to update company: {str(e)}"}
        finally:
            cursor.close()

    @staticmethod
    def delete(company_id):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("DELETE FROM company WHERE id = %s", (company_id,))
            db.commit()
            return {"message": "Company deleted successfully"}
        except Exception as e:
            return {"error": f"Failed to delete company: {str(e)}"}
        finally:
            cursor.close()
