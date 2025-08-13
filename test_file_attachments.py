import unittest
from config import tickets_collection
from bson import ObjectId

class FileAttachmentUnitTest(unittest.TestCase):

    def setUp(self):
        # Insert a test ticket
        self.test_ticket = {
            "ticket_code": "TKT-UNITATTACH",
            "user": "unit_test_user",
            "issue_title": "Attachment Test",
            "issue_detail": "Testing file attachment update.",
            "priority": "Low",
            "status": "Pending",
            "filename": None
        }
        self.ticket_id = tickets_collection.insert_one(self.test_ticket).inserted_id

    def test_file_attachment_assignment(self):
        # Simulate attaching a file to the ticket
        file_path = "static/uploads/test_attachment.png"
        tickets_collection.update_one(
            {"_id": self.ticket_id},
            {"$set": {"filename": file_path}}
        )
        updated_ticket = tickets_collection.find_one({"_id": self.ticket_id})
        self.assertEqual(updated_ticket["filename"], file_path)

    def tearDown(self):
        tickets_collection.delete_one({"_id": self.ticket_id})

if __name__ == "__main__":
    unittest.main()