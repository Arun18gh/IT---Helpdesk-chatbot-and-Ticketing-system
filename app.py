# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime
import os
from bson.objectid import ObjectId
from config import tickets_collection
from models.tickets import Ticket
from models.user import User

import random
import string

def generate_ticket_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


app = Flask(__name__)
app.secret_key = "darkvolt-superkey"

#Login manager setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    from config import users_collection
    user_data = users_collection.find_one({"_id": ObjectId(user_id)})
    if user_data:
        return User(user_data)
    return None

UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf", "docx", "txt"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.context_processor
def inject_now():
    return {'now': datetime.now}

@app.route("/")
def home_page():
    if current_user.is_authenticated:
        return redirect(url_for("home_redirect"))
    return redirect(url_for("login"))

@app.route("/home")
@login_required
def home_redirect():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    from config import users_collection
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user_data = users_collection.find_one({"username": username})
        if user_data and check_password_hash(user_data["password"], password):
            user = User(user_data)
            login_user(user)
            return redirect(url_for("home_redirect"))
        flash("Invalid credentials", "danger")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "info")
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register_user():
    from config import users_collection
    from werkzeug.security import generate_password_hash
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        existing = users_collection.find_one({'username': username})
        if existing:
            flash("User already exists.", "danger")
        else:
            users_collection.insert_one({
                "username": username,
                "password": generate_password_hash(password),
                "role": "user"
            })
            flash("Registration successful. You can now log in.", "success")
            return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/submit", methods=["GET", "POST"])
@login_required
def submit_ticket():
    if request.method == "POST":
        user = request.form.get("user")          
        email = request.form.get("email")        
        title = request.form.get("issue_title")
        details = request.form.get("issue_detail")
        priority = request.form.get("priority")
        department = request.form.get("department")

        ticket = Ticket(user, email, title, details, priority, department)

        file = request.files.get("file")
        if file and allowed_file(file.filename):
            filename = secure_filename(f"{ticket.ticket_code}_{file.filename}")
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            ticket.attachment = filename

        tickets_collection.insert_one(ticket.to_dict())
        flash(f"✅ Ticket submitted! Your ID: {ticket.ticket_code}", "success")
        return redirect(url_for("submit_ticket"))

    return render_template("submit_ticket.html")



@app.route("/user/tickets")
@login_required
def user_tickets():
    if current_user.role != "user":
        flash("Access denied", "danger")
        return redirect(url_for("home_redirect"))

    tickets = list(tickets_collection.find({"email": current_user.username}).sort("created_at", -1))
    return render_template("user_tickets.html", tickets=tickets)

@app.route("/dashboard")
@login_required
def dashboard():
    if not current_user.is_admin():
        flash("Access denied", "danger")
        return redirect(url_for("home_redirect"))

    all_tickets = list(tickets_collection.find().sort("created_at", -1))
    seen = set()
    filtered = []
    for t in all_tickets:
        key = (t.get("user"), t.get("issue_title", ""), t.get("issue_detail", ""))
        if key not in seen:
            seen.add(key)
            filtered.append(t)

    return render_template("dashboard.html", tickets=filtered)

@app.route("/ticket/<ticket_id>")
@login_required
def view_ticket(ticket_id):
    ticket = tickets_collection.find_one({"ticket_code": ticket_id})
    if not ticket:
        flash("Ticket not found.", "danger")
        return redirect(url_for("home_redirect"))
    return render_template("view_ticket.html", ticket=ticket)

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/analytics")
@login_required
def analytics():
    if not current_user.is_admin():
        flash("Access denied", "danger")
        return redirect(url_for("home_redirect"))

    from collections import Counter
    all_tickets = list(tickets_collection.find({}).sort("created_at", -1))

    departments = [t.get("department") for t in all_tickets if "department" in t]
    priorities = [t.get("priority") for t in all_tickets if "priority" in t]

    dept_data = dict(Counter(departments))
    priority_data = dict(Counter(priorities))

    return render_template("analytics.html",
                           dept_data=dept_data,
                           priority_data=priority_data,
                           no_data=False)

@app.route("/api/chart-data")
def chart_data():
    from collections import Counter
    tickets = list(tickets_collection.find())

    dept_counts = Counter(t.get('department') for t in tickets if 'department' in t)
    prio_counts = Counter(t.get('priority') for t in tickets if 'priority' in t)
    date_counts = Counter(
        datetime.strptime(t['created_at'], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
        for t in tickets if 'created_at' in t and isinstance(t['created_at'], str)
    )
    timeline = [{"date": date, "count": count} for date, count in sorted(date_counts.items())]

    return jsonify({
        "by_department": dept_counts,
        "by_priority": prio_counts,
        "timeline": timeline
    })

@app.route("/delete_ticket/<ticket_code>")
@login_required
def delete_ticket(ticket_code):
    if not current_user.is_admin():
        flash("Access denied", "danger")
        return redirect(url_for("home_redirect"))
    tickets_collection.delete_one({"ticket_code": ticket_code})
    flash("Ticket deleted successfully!", "info")
    return redirect(url_for("dashboard"))

@app.route('/solve_ticket/<ticket_code>')
@login_required
def solve_ticket(ticket_code):
    if not current_user.is_admin():
        flash("Access denied", "danger")
        return redirect(url_for("home_redirect"))
    tickets_collection.update_one({'ticket_code': ticket_code}, {'$set': {'status': 'Solved'}})
    flash("✅ Ticket marked as solved.", "success")
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=True)
