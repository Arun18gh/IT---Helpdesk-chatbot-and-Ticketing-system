# config.py
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["it_helpdesk"]

tickets_collection = db["tickets"]
users_collection = db["users"]    


