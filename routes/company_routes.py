from flask import Blueprint, render_template, request, redirect, send_file
import sqlite3
import os
from config import DATABASE

company_bp = Blueprint("company", __name__, url_prefix="/company")

# Absolute upload path (matches applicant upload folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, '..', 'uploads')


# ======================================
# Company Dashboard
# ======================================
@company_bp.route("/dashboard")
def dashboard():

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    # Active Jobs Count
    cur.execute("SELECT COUNT(*) FROM jobs")
    active_jobs = cur.fetchone()[0]

    # Total Applicants
    cur.execute("SELECT COUNT(*) FROM applications")
    total_applicants = cur.fetchone()[0]

    # Shortlisted Count
    cur.execute("SELECT COUNT(*) FROM applications WHERE status = 'Shortlisted'")
    shortlisted = cur.fetchone()[0]

    conn.close()

    return render_template(
        "company/dashboard.html",
        active_jobs=active_jobs,
        total_applicants=total_applicants,
        shortlisted=shortlisted
    )



# ======================================
# Post Job
# ======================================
@company_bp.route("/post-job", methods=["GET", "POST"])
def post_job():

    if request.method == "POST":
        role = request.form["role"]
        company_name = request.form["company_name"]
        company_id = request.form["company_id"]
        vacancy = request.form["vacancy"]
        job_type = request.form["type"]
        salary = request.form["salary"]
        experience = request.form["experience"]
        description = request.form["desc"]

        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO jobs 
            (role, company_name, company_id, vacancy, type, salary, experience, description) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (role, company_name, company_id, vacancy, job_type, salary, experience, description))

        conn.commit()
        conn.close()

        return render_template(
            "company/post_job.html",
            message="✅ Job Posted Successfully!"
        )

    return render_template("company/post_job.html")


# ======================================
# View All Applications
# ======================================
@company_bp.route("/applications")
def view_applications():

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            applications.id,
            applications.full_name,
            jobs.role,
            applications.status,
            applications.user_id,
            applications.resume_filename
        FROM applications
        JOIN jobs ON applications.job_id = jobs.id
        ORDER BY jobs.role
    """)

    data = cur.fetchall()
    conn.close()

    return render_template("company/applicants_list.html", data=data)
# ======================================
# Delete Application
# ======================================
@company_bp.route("/delete-application/<int:app_id>")
def delete_application(app_id):

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    # Optional: get resume filename before delete
    cur.execute("SELECT resume_filename FROM applications WHERE id = ?", (app_id,))
    result = cur.fetchone()

    if result:
        resume_file = result[0]

        # Delete record
        cur.execute("DELETE FROM applications WHERE id = ?", (app_id,))
        conn.commit()

        # Delete resume file from uploads (optional)
        if resume_file:
            file_path = os.path.join(UPLOAD_FOLDER, resume_file)
            if os.path.exists(file_path):
                os.remove(file_path)

    conn.close()

    return redirect("/company/applications")



# ======================================
# View Resume
# ======================================
@company_bp.route("/view-resume/<filename>")
def view_resume(filename):

    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if os.path.exists(file_path):
        return send_file(file_path)

    return "Resume not found", 404


# ======================================
# Update Application Status
# ======================================
@company_bp.route("/update-status/<int:app_id>/<status>")
def update_status(app_id, status):

    allowed_status = ["Pending", "Shortlisted", "Rejected", "Accepted"]

    if status not in allowed_status:
        return "Invalid status"

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    cur.execute(
        "UPDATE applications SET status = ? WHERE id = ?",
        (status, app_id)
    )

    conn.commit()
    conn.close()

    return redirect("/company/applications")
