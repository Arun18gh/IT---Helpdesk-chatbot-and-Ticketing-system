
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
import os

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["it_helpdesk"]
users = db["users"]

users.delete_many({})

user_list = [
    {
        "username": "arun.admin@darkvolt.com",
        "password": generate_password_hash("arun.admin@123"),
        "role": "admin"
    },
    {
        "username": "naveena.admin@darkvolt.com",
        "password": generate_password_hash("naveena.admin@123"),
        "role": "admin"
    },
    {
        "username": "arun.user@gmail.com",
        "password": generate_password_hash("userpass1"),
        "role": "user"
    },
    {
        "username": "naveena.user@gmail.com",
        "password": generate_password_hash("userpass2"),
        "role": "user"
    }
]


users.insert_many(user_list)
print("✅ Admin and User accounts created successfully!")
