import unittest
from app import app
from config import users_collection

TEST_USERNAME = "test_register_user"
TEST_PASSWORD = "TestReg123"

class UserRegistrationTest(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        users_collection.delete_many({"username": TEST_USERNAME})

    def test_user_registration(self):
        response = self.client.post("/register", data={
            "username": TEST_USERNAME,
            "password": TEST_PASSWORD
        }, content_type='application/x-www-form-urlencoded', follow_redirects=True)

        self.assertIn(b"registration successful", response.data.lower())

        user = users_collection.find_one({"username": TEST_USERNAME})
        self.assertIsNotNone(user)
        self.assertEqual(user["username"], TEST_USERNAME)

    def tearDown(self):
        users_collection.delete_many({"username": TEST_USERNAME})

if __name__ == "__main__":
    unittest.main()
