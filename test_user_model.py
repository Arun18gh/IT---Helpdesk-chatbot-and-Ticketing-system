import unittest
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from bson.objectid import ObjectId

# Connect to MongoDB
MONGO_URI = "mongodb://localhost:27017"
client = MongoClient(MONGO_URI)
db = client["it_helpdesk"]
users_collection = db["users"]


TEST_NAME = "Test User"
TEST_EMAIL = "test_user@example.com"
TEST_PASSWORD = "TestPassword123"

class User:
    def __init__(self, data):
        self.id = str(data["_id"])
        self.name = data["name"]
        self.email = data["email"]
        self.password_hash = data["password"]
        self.role = data.get("role", "user")
    def is_admin(self):
        return self.role == "admin"

def create_user(name, email, password, role="user"):
    password_hash = generate_password_hash(password)
    user_data = {
        "name": name,
        "email": email,
        "password": password_hash,
        "role": role
    }
    users_collection.insert_one(user_data)

def check_credentials(email, password):
    user_data = users_collection.find_one({"email": email})
    if user_data and check_password_hash(user_data["password"], password):
        return User(user_data)
    return None

class UserModelTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        users_collection.delete_many({"email": TEST_EMAIL})
        create_user(TEST_NAME, TEST_EMAIL, TEST_PASSWORD)

    def test_user_created(self):
        user = users_collection.find_one({"email": TEST_EMAIL})
        self.assertIsNotNone(user)
        self.assertEqual(user["name"], TEST_NAME)

    def test_valid_login(self):
        user = check_credentials(TEST_EMAIL, TEST_PASSWORD)
        self.assertIsNotNone(user)
        self.assertEqual(user.email, TEST_EMAIL)

    def test_invalid_password(self):
        user = check_credentials(TEST_EMAIL, "WrongPassword")
        self.assertIsNone(user)

    def test_invalid_email(self):
        user = check_credentials("invalid@example.com", "anything")
        self.assertIsNone(user)

    def test_role_check(self):
        user_data = users_collection.find_one({"email": TEST_EMAIL})
        user = User(user_data)
        self.assertFalse(user.is_admin())

    @classmethod
    def tearDownClass(cls):
        users_collection.delete_many({"email": TEST_EMAIL})

if __name__ == "__main__":
    unittest.main()
