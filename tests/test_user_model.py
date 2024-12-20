import unittest
from app.models.user_model import User
from app.utils.jwt_handler import generate_access_token, decode_token

class TestUserModel(unittest.TestCase):
    def test_add_user(self):
        result = User.add_user("test@example.com", "password123", "applicant")
        self.assertIn("id", result)  # 사용자 ID가 반환되는지 확인

    def test_authenticate(self):
        User.add_user("test@example.com", "password123", "applicant")
        user = User.authenticate("test@example.com", "password123")
        self.assertIsNotNone(user)  # 인증 성공 여부 확인

    def test_jwt_generation(self):
        payload = {"id": 1, "email": "test@example.com", "role": "applicant"}
        token = generate_access_token(payload)
        decoded = decode_token(token)
        self.assertEqual(decoded["email"], "test@example.com")  # 디코딩 확인

if __name__ == "__main__":
    unittest.main()
