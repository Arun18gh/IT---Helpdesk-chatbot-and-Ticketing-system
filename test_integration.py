import unittest
from app import app
from config import users_collection, tickets_collection
from werkzeug.security import generate_password_hash

TEST_USERNAME = "integration_test_user"
TEST_PASSWORD = "TestPass123"
TEST_EMAIL = "integration@example.com"

class HelpdeskIntegrationTest(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        users_collection.delete_many({"username": TEST_USERNAME})
        tickets_collection.delete_many({"user": TEST_USERNAME})
        users_collection.insert_one({
            "username": TEST_USERNAME,
            "password": generate_password_hash(TEST_PASSWORD),
            "role": "user"
        })

    def test_user_login_and_ticket_submission(self):
        login_response = self.client.post("/login", data={
            "username": TEST_USERNAME,
            "password": TEST_PASSWORD
        }, content_type='application/x-www-form-urlencoded', follow_redirects=True)
        self.assertIn(b"home", login_response.data.lower())

        submit_response = self.client.post("/submit", data={
            "user": TEST_USERNAME,
            "email": TEST_EMAIL,
            "issue_title": "Test Issue",
            "issue_detail": "This is a test integration issue.",
            "priority": "High",
            "department": "IT"
        }, content_type='application/x-www-form-urlencoded', follow_redirects=True)
        self.assertIn(b"ticket submitted", submit_response.data.lower())

    def tearDown(self):
        users_collection.delete_many({"username": TEST_USERNAME})
        tickets_collection.delete_many({"user": TEST_USERNAME})

if __name__ == "__main__":
    unittest.main()
