from flask import Blueprint, render_template, request, redirect, send_file, session,send_from_directory
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
@company_bp.route("/add-details", methods=["GET", "POST"])
def add_details():

    if session.get("role") != "company":
        return redirect("/login")

    if request.method == "POST":

        company_name = request.form["company_name"]
        industry = request.form["industry"]
        website = request.form["website"]
        location = request.form["location"]
        description = request.form["description"]

        with sqlite3.connect(DATABASE, timeout=10) as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO company_details
                (user_id, company_name, industry, website, location, description)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                session["user_id"],
                company_name,
                industry,
                website,
                location,
                description
            ))
            conn.commit()

        # 🔥 STORE IMPORTANT DATA IN SESSION
        session["company_name"] = company_name
        session["verified"] = 0

        return redirect("/company/profile")

    return render_template("company/add_details.html")
@company_bp.route("/dashboard")
def dashboard():

    # 🔐 Protect route
    if session.get("role") != "company":
        return redirect("/login")

    company_id = session["user_id"]

    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # 🔎 Check if company details exist
        cur.execute("SELECT * FROM company_details WHERE user_id = ?", (company_id,))
        details = cur.fetchone()

        # 🚨 If no details → force to add
        if not details:
            return redirect("/company/add-details")

        # 🔥 Load important details into session (optional but recommended)
        session["company_name"] = details["company_name"]
        session["verified"] = details["verified"]

        # 📊 Count only this company's jobs
        cur.execute("SELECT COUNT(*) FROM jobs WHERE company_id = ?", (company_id,))
        active_jobs = cur.fetchone()[0]

        # 👥 Count applicants for this company's jobs
        cur.execute("""
            SELECT COUNT(*) FROM applications
            WHERE job_id IN (
                SELECT id FROM jobs WHERE company_id = ?
            )
        """, (company_id,))
        total_applicants = cur.fetchone()[0]

        # ⭐ Shortlisted count
        cur.execute("""
            SELECT COUNT(*) FROM applications
            WHERE status = 'Shortlisted'
            AND job_id IN (
                SELECT id FROM jobs WHERE company_id = ?
            )
        """, (company_id,))
        shortlisted = cur.fetchone()[0]

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

    # 🔐 Protect route
    if session.get("role") != "company":
        return redirect("/login")

    company_id = session["user_id"]

    # 🔎 Check verification status
    with sqlite3.connect(DATABASE, timeout=10) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        cur.execute("SELECT verified FROM company_details WHERE user_id = ?", (company_id,))
        company = cur.fetchone()

        # ❌ If not verified → block posting
        if not company or company["verified"] != 1:
            return render_template(
                "company/post_job.html",
                error="⚠ Your company is not verified. You cannot post jobs."
            )

        # ✅ If POST and verified → allow insert
        if request.method == "POST":

            role = request.form["role"]
            vacancy = request.form["vacancy"]
            job_type = request.form["type"]
            salary = request.form["salary"]
            experience = request.form["experience"]
            description = request.form["desc"]

            cur.execute("""
                INSERT INTO jobs 
                (role, company_name, company_id, vacancy, type, salary, experience, description) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                role,
                session["company_name"],
                company_id,
                vacancy,
                job_type,
                salary,
                experience,
                description
            ))

            conn.commit()

            return render_template(
                "company/post_job.html",
                message="✅ Job Posted Successfully!"
            )

    return render_template("company/post_job.html")
# profile 
# ======================================
# Company Profile
# ======================================
@company_bp.route("/profile")
def profile():

    if session.get("role") != "company":
        return redirect("/login")

    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        cur.execute("""
            SELECT users.name, users.email, company_details.*
            FROM users
            JOIN company_details
            ON users.id = company_details.user_id
            WHERE users.id = ?
        """, (session["user_id"],))

        company = cur.fetchone()

    return render_template("company/profile.html", company=company)



@company_bp.route("/update-profile", methods=["POST"])
def update_company_profile():

    # 🔐 Proper Role Check
    if session.get("role") != "company":
        return redirect("/login")

    name = request.form["company_name"]
    email = request.form["email"]

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    # 🔥 Update USERS table (not companies)
    cur.execute("""
        UPDATE users
        SET name = ?, email = ?
        WHERE id = ?
    """, (name, email, session["user_id"]))

    conn.commit()
    conn.close()

    # 🔥 Update session so navbar shows new name instantly
    session["company_name"] = name

    return redirect("/company/profile")

# ======================================
# View All Applications
# ======================================
@company_bp.route("/applications")
def view_applications():

    # 🔐 Security check
    if session.get("role") != "company":
        return redirect("/login")

    company_id = session["user_id"]   # Logged in company

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            applications.id,
            applications.full_name,
            jobs.role,
            applications.status,
            applications.resume_filename
        FROM applications
        INNER JOIN jobs 
            ON applications.job_id = jobs.id
        WHERE jobs.company_id = ?
        ORDER BY applications.id DESC
    """, (company_id,))

    data = cur.fetchall()
    conn.close()

    return render_template("company/applicants_list.html", data=data)


@company_bp.route("/view-resume/<filename>")
def view_resume_file(filename):
    return send_from_directory("uploads", filename)
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
