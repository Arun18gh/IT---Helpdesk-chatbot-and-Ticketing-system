import unittest
from app import app
from config import users_collection
from werkzeug.security import generate_password_hash

class InvalidLoginIntegrationTest(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Insert a valid user
        self.username = "invalid_login_test"
        self.correct_password = "ValidPass123"
        self.wrong_password = "WrongPass456"

        users_collection.delete_many({"username": self.username})
        users_collection.insert_one({
            "username": self.username,
            "password": generate_password_hash(self.correct_password),
            "role": "user"
        })

    def test_login_with_wrong_password(self):
        response = self.client.post("/login", data={
            "username": self.username,
            "password": self.wrong_password
        }, content_type='application/x-www-form-urlencoded', follow_redirects=True)

        self.assertIn(b"invalid credentials", response.data.lower())

    def tearDown(self):
        users_collection.delete_many({"username": self.username})

if __name__ == "__main__":
    unittest.main()
