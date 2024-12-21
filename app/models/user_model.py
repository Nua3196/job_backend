import base64
from app.utils.db import get_db
import re
import os

class User:
    def __init__(self, id, email, password, role, company=None):
        self.id = id
        self.email = email
        self.password = password  # Base64로 인코딩된 비밀번호
        self.role = role
        self.company = company

    @staticmethod
    def encode_password(password):
        """
        비밀번호를 Base64로 인코딩하는 메서드

        Args:
            password (str): 평문 비밀번호

        Returns:
            str: Base64로 인코딩된 비밀번호
        """
        salt = os.urandom(16)  # 16바이트 랜덤 Salt 생성
        salted_password = salt + password.encode('utf-8')  # Salt 추가
        return base64.b64encode(salted_password).decode('utf-8')
    
    @staticmethod
    def is_valid_email(email):
        """
        이메일 형식을 검증하는 함수.

        Args:
            email (str): 입력된 이메일

        Returns:
            bool: 이메일이 유효하면 True, 그렇지 않으면 False
        """
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(email_regex, email) is not None

    @staticmethod
    def get_user_by_email(email):
        """
        이메일을 기준으로 데이터베이스에서 사용자 정보를 조회하는 메서드

        Args:
            email (str): 조회할 사용자의 이메일

        Returns:
            User: 사용자 정보가 담긴 User 객체
            None: 해당 이메일의 사용자가 존재하지 않는 경우
        """
        db = get_db()
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id, email, password, role, company FROM user WHERE email = %s", (email,))
            user_data = cursor.fetchone()
            if user_data:
                return User(**user_data)  # User 객체로 변환
            return None
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def add_user(email, password, role, company=None):
        """
        사용자를 user 테이블에 추가하거나 기존 사용자 ID를 반환.
        Args:
            email (str): 사용자 이메일
            password (str): 평문 비밀번호
            role (str): 사용자 역할 ('admin', 'employer', 'applicant' 등)
            company (int, optional): 회사 ID (기본값: None)
        Returns:
            dict: 사용자 ID 또는 오류 메시지
        """
        db = get_db()
        cursor = db.cursor()

        # 이메일 형식 검증
        if not User.is_valid_email(email):
            return {"error": f"Invalid email format: {email}"}

        # employer인 경우 company 필드 필수
        if role == 'employer' and not company:
            return {"error": "Company ID is required for employers"}

        # company 유효성 검증
        if company and not Company.validate(company):
            return {"error": f"Invalid company ID: {company}"}

        try:
            # 이미 존재하는 이메일인지 확인
            cursor.execute("SELECT id FROM user WHERE email = %s", (email,))
            result = cursor.fetchone()

            if result:
                return {"error": f"Email already exists. User ID: {result[0]}"}

            # 비밀번호 Base64 인코딩
            encoded_password = User.encode_password(password)

            # 사용자 추가
            cursor.execute("""
                INSERT INTO user (email, password, role, company)
                VALUES (%s, %s, %s, %s)
            """, (email, encoded_password, role, company))
            db.commit()

            user_id = cursor.lastrowid
            return {"id": user_id, "message": f"User {email} added successfully"}
        except Exception as e:
            return {"error": f"Failed to add user: {str(e)}"}
        finally:
            cursor.close()
            db.close()


    @staticmethod
    def verify_password(input_password, stored_password):
        """
        비밀번호를 검증하는 메서드
        Args:
            input_password (str): 입력된 평문 비밀번호
            stored_password (str): 데이터베이스에 저장된 Base64 비밀번호 해시

        Returns:
            bool: 비밀번호가 일치하면 True, 아니면 False
        """
        decoded_stored = base64.b64decode(stored_password.encode('utf-8'))
        salt = decoded_stored[:16]  # 저장된 Salt 추출
        salted_input_password = salt + input_password.encode('utf-8')
        encoded_input_password = base64.b64encode(salted_input_password).decode('utf-8')
        return encoded_input_password == stored_password

    @classmethod
    def authenticate(cls, email, password):
        """
        이메일과 비밀번호를 검증하여 사용자를 인증하는 메서드

        Args:
            email (str): 사용자의 이메일
            password (str): 평문 비밀번호

        Returns:
            User: 인증된 사용자 정보가 담긴 User 객체
            None: 인증 실패 시
        """
        user = cls.get_user_by_email(email)

        if not user:
            print(f"User with email {email} not found in the database.")
            return None

        # 저장된 비밀번호와 입력된 비밀번호 출력
        print(f"Stored password: {user.password}")
        print(f"Input password: {password}")

        # 비밀번호 검증
        if cls.verify_password(password, user.password):
            print("Password verified successfully.")
            return user
        else:
            print("Password verification failed.")
        # if user and cls.verify_password(password, user.password):
        #     return user  # 인증 성공
        return None  # 인증 실패

    def to_dict(self):
        """
        User 객체를 딕셔너리로 변환하는 메서드

        Returns:
            dict: 사용자 정보를 딕셔너리 형태로 반환
        """
        return {
            'id': self.id,
            'email': self.email,
            'role': self.role,
            'company': self.company
        }

    @staticmethod
    def get_user_by_id(user_id):
        """
        사용자 ID를 기준으로 사용자 정보를 조회
        Args:
            user_id (int): 조회할 사용자 ID
        Returns:
            User: User 객체
        """
        db = get_db()
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id, email, role, company, created_at FROM user WHERE id = %s", (user_id,))
            user_data = cursor.fetchone()
            if user_data:
                return User(**user_data)  # User 객체로 변환
            return None
        finally:
            cursor.close()

    @staticmethod
    def update_user(user_id, fields):
        """
        사용자의 특정 필드를 업데이트
        Args:
            user_id (int): 업데이트할 사용자 ID
            fields (dict): 업데이트할 필드와 값
        Returns:
            dict: 성공 메시지 또는 에러 메시지
        """
        db = get_db()
        cursor = db.cursor()

        # company 유효성 검증
        if 'company' in fields and not Company.validate(fields['company']):
            return {"error": f"Invalid company ID: {fields['company']}"}

        try:
            set_clause = ", ".join(f"{key} = %s" for key in fields.keys())
            values = list(fields.values()) + [user_id]
            cursor.execute(f"UPDATE user SET {set_clause} WHERE id = %s", values)
            db.commit()
            return {"message": "User updated successfully"}
        except Exception as e:
            return {"error": f"Failed to update user: {str(e)}"}
        finally:
            cursor.close()


    @staticmethod
    def delete_user(user_id):
        """
        사용자를 데이터베이스에서 삭제
        Args:
            user_id (int): 삭제할 사용자 ID
        Returns:
            dict: 성공 메시지 또는 에러 메시지
        """
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("DELETE FROM user WHERE id = %s", (user_id,))
            db.commit()
            return {"message": "User deleted successfully"}
        except Exception as e:
            return {"error": f"Failed to delete user: {str(e)}"}
        finally:
            cursor.close()

    @staticmethod
    def toggle_bookmark(user_id, job_id):
        """
        북마크 추가/제거 (토글)
        Args:
            user_id (int): 사용자 ID
            job_id (int): 공고 ID
        Returns:
            dict: 성공 메시지 또는 에러 메시지
        """
        db = get_db()
        cursor = db.cursor()
        try:
            # 북마크 존재 여부 확인
            cursor.execute("SELECT 1 FROM bookmark WHERE user = %s AND job = %s", (user_id, job_id))
            if cursor.fetchone():
                # 북마크 제거
                cursor.execute("DELETE FROM bookmark WHERE user = %s AND job = %s", (user_id, job_id))
                db.commit()
                return {"message": "Bookmark removed"}
            else:
                # 북마크 추가
                cursor.execute("INSERT INTO bookmark (user, job) VALUES (%s, %s)", (user_id, job_id))
                db.commit()
                return {"message": "Bookmark added"}
        except Exception as e:
            return {"error": f"Failed to toggle bookmark: {str(e)}"}
        finally:
            cursor.close()

    @staticmethod
    def get_bookmarks(user_id):
        """
        사용자의 북마크 조회
        Args:
            user_id (int): 사용자 ID
        Returns:
            list: 북마크 목록
        """
        db = get_db()
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT job.* FROM job
                JOIN bookmark ON job.id = bookmark.job
                WHERE bookmark.user = %s
            """, (user_id,))
            return cursor.fetchall()
        finally:
            cursor.close()

    @staticmethod
    def add_application(user_id, job_id, content):
        """
        지원 내역 추가 (Application 모델 호출)
        Args:
            user_id (int): 사용자 ID
            job_id (int): 공고 ID
            content (str): 지원 내용
        Returns:
            dict: 성공 메시지 또는 에러 메시지
        """
        return Application.add(user_id, job_id, content)

    @staticmethod
    def get_applications(user_id):
        """
        사용자의 지원 내역 조회 (Application 모델 호출)
        Args:
            user_id (int): 사용자 ID
        Returns:
            list: 지원 내역 목록
        """
        return Application.get_by_user(user_id)

    @staticmethod
    def delete_application(user_id, job_id):
        """
        지원 내역 삭제 (Application 모델 호출)
        Args:
            user_id (int): 사용자 ID
            job_id (int): 공고 ID
        Returns:
            dict: 성공 메시지 또는 에러 메시지
        """
        return Application.delete(user_id, job_id)