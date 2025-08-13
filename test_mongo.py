from pymongo import MongoClient
import json

client = MongoClient("mongodb://localhost:27017/")
db = client["it_helpdesk"] 

print("Tickets:")
for ticket in db.tickets.find():
    print(json.dumps(ticket, indent=2, default=str))

print("\nUsers:")
for user in db.users.find():
    print(json.dumps(user, indent=2, default=str))



