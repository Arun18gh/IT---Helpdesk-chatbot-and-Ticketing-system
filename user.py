# models/user.py
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_dict):
        self.id = str(user_dict["_id"])
        self.username = user_dict["username"]
        self.role = user_dict.get("role", "user")  # default to 'user'

    def is_admin(self):
        return self.role == "admin"
