from app.utils.db import get_db

class Company:
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
