from flask import Blueprint, render_template, request, redirect
import sqlite3
from config import DATABASE

company_bp = Blueprint("company", __name__)

# Company Dashboard
@company_bp.route("/dashboard")
def dashboard():
    return render_template("company/dashboard.html")

# Post Job
@company_bp.route("/post-job", methods=["GET", "POST"])
def post_job():
    message = ""

    if request.method == "POST":
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO jobs (title, description, company_id) VALUES (?, ?, ?)",
            (request.form["title"], request.form["desc"], request.form["company_id"])
        )
        conn.commit()
        conn.close()

        message = "✅ Job posted successfully!"

    return render_template("company/post_job.html", message=message)

# View Applicants
@company_bp.route("/applicants")
def applicants():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("""
        SELECT a.id, u.name, j.title, a.status, u.id
        FROM applications a
        JOIN users u ON a.user_id = u.id
        JOIN jobs j ON a.job_id = j.id
    """)
    data = cur.fetchall()
    conn.close()
    return render_template("company/applicants.html", data=data)

# Shortlist Applicant
@company_bp.route("/shortlist/<int:app_id>/<int:user_id>")
def shortlist(app_id, user_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    cur.execute(
        "UPDATE applications SET status = 'Shortlisted' WHERE id = ?",
        (app_id,)
    )

    cur.execute(
        "INSERT INTO notifications (user_id, message) VALUES (?, ?)",
        (user_id, "🎉 You are shortlisted for the interview")
    )

    conn.commit()
    conn.close()

    return redirect("/company/applicants")
