import unittest
import time
from bson.objectid import ObjectId
from datetime import datetime, timezone
from models.tickets import Ticket
from config import tickets_collection

TEST_USER = "Test User"
TEST_EMAIL = "test@example.com"
TEST_TITLE = "Login Issue"
TEST_DETAIL = "Unable to login"
TEST_PRIORITY = "High"
TEST_DEPT = "IT"

class TicketModelTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ticket = Ticket(TEST_USER, TEST_EMAIL, TEST_TITLE, TEST_DETAIL, TEST_PRIORITY, TEST_DEPT)
        cls.ticket_id = tickets_collection.insert_one(cls.ticket.to_dict()).inserted_id
        time.sleep(1)

    def test_ticket_created(self):
        ticket = tickets_collection.find_one({"_id": ObjectId(self.ticket_id)})
        self.assertIsNotNone(ticket)
        self.assertEqual(ticket["user"], TEST_USER)
        self.assertIn("TKT-", ticket["ticket_code"])

    def test_ticket_has_priority_and_department(self):
        ticket = tickets_collection.find_one({"_id": ObjectId(self.ticket_id)})
        self.assertEqual(ticket["priority"], TEST_PRIORITY)
        self.assertEqual(ticket["department"], TEST_DEPT)

    def test_ticket_code_format(self):
        ticket = tickets_collection.find_one({"_id": ObjectId(self.ticket_id)})
        self.assertTrue(ticket["ticket_code"].startswith("TKT-"))
        self.assertEqual(len(ticket["ticket_code"]), 10)

    @classmethod
    def tearDownClass(cls):
        tickets_collection.delete_one({"_id": ObjectId(cls.ticket_id)})

if __name__ == "__main__":
    unittest.main()
