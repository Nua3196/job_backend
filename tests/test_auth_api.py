import unittest
from app import create_app
from app.models.user_model import User

class TestAuthAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()  # Flask 애플리케이션 생성
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        User.add_user("test@example.com", "password123", "applicant")  # 테스트 사용자 추가

    def tearDown(self):
        self.app_context.pop()

    def test_signup(self):
        response = self.client.post("/api/auth/signup", json={
            "email": "newuser@example.com",
            "password": "newpassword",
            "role": "creator"
        })
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        response = self.client.post("/api/auth/login", json={
            "email": "test@example.com",
            "password": "password123"
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", data)

    def test_refresh(self):
        # 먼저 로그인하여 Refresh 토큰 확보
        login_response = self.client.post("/api/auth/login", json={
            "email": "test@example.com",
            "password": "password123"
        })
        refresh_token = login_response.get_json()["refresh_token"]

        # Refresh 토큰을 사용해 Access 토큰 갱신
        response = self.client.post("/api/auth/refresh", json={"refresh_token": refresh_token})
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", data)

if __name__ == "__main__":
    unittest.main()
