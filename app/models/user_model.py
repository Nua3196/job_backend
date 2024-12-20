import base64
from app.utils.db import get_db

class User:
    def __init__(self, id, email, password, role):
        self.id = id
        self.email = email
        self.password = password  # Base64로 인코딩된 비밀번호
        self.role = role

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
            cursor.execute("SELECT id, email, password, role FROM user WHERE email = %s", (email,))
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
            role (str): 사용자 역할 ('admin', 'creator', 'applicant' 등)
            company (int, optional): 회사 ID (기본값: None)

        Returns:
            dict: 사용자 ID 또는 오류 메시지
        """
        db = get_db()
        cursor = db.cursor()

        # 이메일 형식 검증
        if not User.is_valid_email(email):
            return {"error": f"Invalid email format: {email}"}

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
        if user and user.password == cls.encode_password(password):
            return user  # 인증 성공
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
            'role': self.role
        }

class Bookmark:
    def __init__(self, id, user, job, created)