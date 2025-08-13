import os
import random
from config import tickets_collection


attachment_folder = "static/uploads"
files = os.listdir(attachment_folder)
valid_files = [f for f in files if f.lower().endswith(('.pdf', '.jpg', '.png', '.docx', '.txt', '.xlsx'))]

# Get all tickets
tickets = list(tickets_collection.find())

print(f"🔄 Assigning attachments to {len(tickets)} tickets...")

for ticket in tickets:
    attachment = random.choice(valid_files)
    tickets_collection.update_one(
        {"_id": ticket["_id"]},
        {"$set": {"attachment": f"/static/uploads/{attachment}"}}
    )

print("✅ Attachments assigned successfully to all tickets.")
