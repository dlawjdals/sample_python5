import unittest

from fastapi.testclient import TestClient

from secure_main import app


class TestSecureApp(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_root(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("message", resp.json())

    def test_health(self):
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"status": "ok"})

    def test_user_found(self):
        resp = self.client.get("/users/hong_gildong")
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertEqual(body["username"], "hong_gildong")
        self.assertIn("email", body)

    def test_user_not_found(self):
        resp = self.client.get("/users/does_not_exist")
        self.assertEqual(resp.status_code, 404)


if __name__ == "__main__":
    unittest.main()
