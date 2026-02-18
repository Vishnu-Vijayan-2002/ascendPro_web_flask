from flask import Blueprint, render_template, redirect, url_for
import sqlite3
from config import DATABASE

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# ==============================
# Admin Dashboard
# ==============================
@admin_bp.route("/dashboard")
def dashboard():

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    # Total users
    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]

    # Pending users
    cur.execute("SELECT COUNT(*) FROM users WHERE approved = 0")
    pending_users = cur.fetchone()[0]

    # Active jobs
    cur.execute("SELECT COUNT(*) FROM jobs")
    active_jobs = cur.fetchone()[0]

    # Companies (case safe)
    cur.execute("SELECT COUNT(*) FROM users WHERE LOWER(role) = 'company'")
    total_companies = cur.fetchone()[0]

    # Role-wise count (Pie Chart)
    cur.execute("SELECT LOWER(role), COUNT(*) FROM users GROUP BY LOWER(role)")
    role_data = cur.fetchall()

    # Initialize counts
    role_counts = {
        "admin": 0,
        "company": 0,
        "applicant": 0
    }

    for r in role_data:
        role_counts[r[0]] = r[1]

    conn.close()

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        pending_users=pending_users,
        active_jobs=active_jobs,
        total_companies=total_companies,
        role_counts=role_counts
    )


# ==============================
# Pending Users
# ==============================
@admin_bp.route("/pending-users")
def pending_users():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, email, role 
        FROM users 
        WHERE approved = 0
        ORDER BY id DESC
    """)
    users = cur.fetchall()

    conn.close()
    return render_template("admin/users.html", users=users)


# ==============================
# Approve User
# ==============================
@admin_bp.route("/approve/<int:uid>")
def approve(uid):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    cur.execute("UPDATE users SET approved = 1 WHERE id = ?", (uid,))
    conn.commit()
    conn.close()

    return redirect("/admin/pending-users")


# ==============================
# Manage Applicants (All Applicants)
# ==============================
# ==============================
# Manage Applicants (All Applicants)
# ==============================
@admin_bp.route("/users")
def manage_users():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Debug (optional - remove later)
    print("Using database:", DATABASE)

    cur.execute("""
        SELECT id, name, email, role, approved
        FROM users
        WHERE role = ?
        ORDER BY id DESC
    """, ("applicant",))

    users = cur.fetchall()

    conn.close()

    return render_template(
        "admin/manage_users.html",
        users=users
    )

# Toggle status
@admin_bp.route("/update-status/<int:user_id>")
def update_status(user_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    cur.execute("SELECT approved FROM users WHERE id = ?", (user_id,))
    current = cur.fetchone()[0]

    new_status = 0 if current == 1 else 1

    cur.execute("UPDATE users SET approved = ? WHERE id = ?", (new_status, user_id))
    conn.commit()
    conn.close()

    return redirect("/admin/users")


# Delete user
@admin_bp.route("/delete-user/<int:user_id>")
def delete_user(user_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

    return redirect("/admin/users")


# ==============================
# View Jobs
# ==============================
@admin_bp.route("/jobs")
def jobs():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
        SELECT id, role, company_name, company_id,
               vacancy, type, salary, experience,
               description, created_at
        FROM jobs
        ORDER BY datetime(created_at) DESC
    """)
    jobs = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM jobs")
    total_jobs = cur.fetchone()[0]

    conn.close()

    return render_template(
        "admin/jobs.html",
        jobs=jobs,
        total_jobs=total_jobs
    )


# ==============================
# Delete Job
# ==============================
@admin_bp.route("/delete-job/<int:job_id>")
def delete_job(job_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    cur.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
    conn.commit()
    conn.close()

    return redirect("/admin/jobs")


# ==============================
# View Applications
# ==============================
@admin_bp.route("/applications")
def applications():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
        SELECT id, user_id, job_id, status, applied_at
        FROM applications
        ORDER BY datetime(applied_at) DESC
    """)
    applications = cur.fetchall()

    conn.close()

    return render_template(
        "admin/applications.html",
        applications=applications
    )
# companies
@admin_bp.route("/companies")
def companies():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, email, approved
        FROM users
        WHERE role = 'company'
        ORDER BY id DESC
    """)
    companies = cur.fetchall()

    conn.close()

    return render_template(
        "company/companies_manage.html",
        companies=companies
    )
@admin_bp.route("/reject-company/<int:company_id>")
def reject_company(company_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    # Set approved = 0 (Pending)
    cur.execute("""
        UPDATE users
        SET approved = 0
        WHERE id = ? AND role = 'company'
    """, (company_id,))

    conn.commit()
    conn.close()

    return redirect(url_for("admin.companies"))
@admin_bp.route("/approve-company/<int:company_id>")
def approve_company(company_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    # Set approved = 1
    cur.execute("""
        UPDATE users
        SET approved = 1
        WHERE id = ? AND role = 'company'
    """, (company_id,))

    conn.commit()
    conn.close()

    return redirect(url_for("admin.companies"))

def delete_company(company_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    cur.execute("DELETE FROM users WHERE id = ?", (company_id,))
    conn.commit()
    conn.close()

    return redirect("/admin/companies")