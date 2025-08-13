import unittest
from app import app
from config import users_collection, tickets_collection
from werkzeug.security import generate_password_hash

ADMIN_USERNAME = "admin_test"
ADMIN_PASSWORD = "Admin123"
USER_USERNAME = "user_test"
USER_PASSWORD = "User123"

class AdminIntegrationTest(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

        users_collection.delete_many({"username": {"$in": [ADMIN_USERNAME, USER_USERNAME]}})
        tickets_collection.delete_many({"user": USER_USERNAME})

        users_collection.insert_many([
            {
                "username": ADMIN_USERNAME,
                "password": generate_password_hash(ADMIN_PASSWORD),
                "role": "admin"
            },
            {
                "username": USER_USERNAME,
                "password": generate_password_hash(USER_PASSWORD),
                "role": "user"
            }
        ])

        tickets_collection.insert_one({
            "user": USER_USERNAME,
            "email": "user@example.com",
            "issue_title": "Sample Ticket",
            "issue_detail": "This needs fixing.",
            "priority": "High",
            "department": "IT",
            "status": "Pending",
            "ticket_code": "TKT-ADMIN1"
        })

    def test_admin_login_and_mark_ticket_solved(self):
        login_response = self.client.post("/login", data={
            "username": ADMIN_USERNAME,
            "password": ADMIN_PASSWORD
        }, content_type='application/x-www-form-urlencoded', follow_redirects=True)

        self.assertIn(b"dashboard", login_response.data.lower())

        solve_response = self.client.get("/solve_ticket/TKT-ADMIN1", follow_redirects=True)
        self.assertIn(b"ticket marked as solved", solve_response.data.lower())

        updated_ticket = tickets_collection.find_one({"ticket_code": "TKT-ADMIN1"})
        self.assertEqual(updated_ticket["status"], "Solved")

    def tearDown(self):
        users_collection.delete_many({"username": {"$in": [ADMIN_USERNAME, USER_USERNAME]}})
        tickets_collection.delete_many({"user": USER_USERNAME})

if __name__ == "__main__":
    unittest.main()