from flask import Blueprint, render_template, redirect
import sqlite3
from config import DATABASE

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/dashboard")
def dashboard():
    return render_template("admin/dashboard.html")

@admin_bp.route("/pending-users")
def pending_users():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT id,name,email,role FROM users WHERE approved=0")
    users = cur.fetchall()
    conn.close()
    return render_template("admin/users.html", users=users)

@admin_bp.route("/approve/<int:uid>")
def approve(uid):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("UPDATE users SET approved=1 WHERE id=?", (uid,))
    conn.commit()
    conn.close()
    return redirect("/admin/pending-users")

@admin_bp.route("/jobs")
def jobs():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM jobs")
    jobs = cur.fetchall()
    conn.close()
    return render_template("admin/jobs.html", jobs=jobs)
