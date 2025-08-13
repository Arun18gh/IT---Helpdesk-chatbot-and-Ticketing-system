# models/tickets.py
import random
import string
from datetime import datetime

class Ticket:
    def __init__(self, user, email, issue_title, issue_detail, priority, department, filename=None):
        self.user = user
        self.email = email
        self.issue_title = issue_title
        self.issue_detail = issue_detail
        self.priority = priority
        self.department = department
        self.filename = filename
        self.ticket_code = self._generate_ticket_code()
        self.created_at = datetime.now()

    def _generate_ticket_code(self):
        prefix = "TKT-"
        suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return prefix + suffix

    def to_dict(self):
        return {
            "user": self.user,
            "email": self.email,
            "issue_title": self.issue_title,
            "issue_detail": self.issue_detail,
            "priority": self.priority,
            "department": self.department,
            "filename": self.filename,
            "ticket_code": self.ticket_code,
            "created_at": self.created_at
        }
