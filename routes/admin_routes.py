from flask import Blueprint, render_template, redirect, url_for, session
import sqlite3
from config import DATABASE

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# ==============================
# ADMIN PROTECTION HELPER
# ==============================
def admin_required():
    if session.get("role") != "admin":
        return False
    return True


# ==============================
# Admin Dashboard
# ==============================
@admin_bp.route("/dashboard")
def dashboard():

    if not admin_required():
        return redirect("/login")

    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM users")
        total_users = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM users WHERE approved = 0")
        pending_users = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM jobs")
        active_jobs = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM users WHERE role = 'company'")
        total_companies = cur.fetchone()[0]

        cur.execute("SELECT role, COUNT(*) FROM users GROUP BY role")
        role_data = cur.fetchall()

    role_counts = {"admin": 0, "company": 0, "applicant": 0}

    for r in role_data:
        role_counts[r[0]] = r[1]

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

    if not admin_required():
        return redirect("/login")

    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        cur.execute("""
            SELECT id, name, email, role
            FROM users
            WHERE approved = 0
            ORDER BY id DESC
        """)
        users = cur.fetchall()

    return render_template("admin/users.html", users=users)


# ==============================
# Approve User
# ==============================
@admin_bp.route("/approve/<int:uid>")
def approve_user(uid):

    if not admin_required():
        return redirect("/login")

    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute("UPDATE users SET approved = 1 WHERE id = ?", (uid,))
        conn.commit()

    return redirect("/admin/pending-users")


# ==============================
# Companies (With Verification)
# ==============================
@admin_bp.route("/companies")
def companies():

    if not admin_required():
        return redirect("/login")

    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        cur.execute("""
            SELECT users.id, users.name, users.email, users.approved,
                   company_details.verified
            FROM users
            LEFT JOIN company_details
            ON users.id = company_details.user_id
            WHERE users.role = 'company'
            ORDER BY users.id DESC
        """)
        companies = cur.fetchall()

    return render_template("admin/companies_manage.html", companies=companies)


# ==============================
# Verify Company (Official)
# ==============================
@admin_bp.route("/verify-company/<int:user_id>")
def verify_company(user_id):

    if not admin_required():
        return redirect("/login")

    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()

        cur.execute("""
            UPDATE company_details
            SET verified = 1
            WHERE user_id = ?
        """, (user_id,))

        conn.commit()

    return redirect(url_for("admin.companies"))


# ==============================
# Delete Company
# ==============================
@admin_bp.route("/delete-company/<int:company_id>")
def delete_company(company_id):

    if not admin_required():
        return redirect("/login")

    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()

        cur.execute("DELETE FROM users WHERE id = ?", (company_id,))
        cur.execute("DELETE FROM company_details WHERE user_id = ?", (company_id,))
        conn.commit()

    return redirect(url_for("admin.companies"))


# ==============================
# Manage Applicants
# ==============================
@admin_bp.route("/users")
def manage_users():

    if not admin_required():
        return redirect("/login")

    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        cur.execute("""
            SELECT id, name, email, role, approved
            FROM users
            WHERE role = 'applicant'
            ORDER BY id DESC
        """)
        users = cur.fetchall()

    return render_template("admin/manage_users.html", users=users)


# ==============================
# Toggle User Status
# ==============================
@admin_bp.route("/update-status/<int:user_id>")
def update_user_status(user_id):

    if not admin_required():
        return redirect("/login")

    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()

        cur.execute("SELECT approved FROM users WHERE id = ?", (user_id,))
        current = cur.fetchone()[0]

        new_status = 0 if current == 1 else 1

        cur.execute("UPDATE users SET approved = ? WHERE id = ?", (new_status, user_id))
        conn.commit()

    return redirect("/admin/users")


# ==============================
# Delete User
# ==============================
@admin_bp.route("/delete-user/<int:user_id>")
def delete_user(user_id):

    if not admin_required():
        return redirect("/login")

    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()

    return redirect("/admin/users")


# ==============================
# View Jobs
# ==============================
@admin_bp.route("/jobs")
def jobs():

    if not admin_required():
        return redirect("/login")

    with sqlite3.connect(DATABASE) as conn:
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

    return render_template("admin/jobs.html", jobs=jobs, total_jobs=total_jobs)


# ==============================
# Delete Job
# ==============================
@admin_bp.route("/delete-job/<int:job_id>")
def delete_job(job_id):

    if not admin_required():
        return redirect("/login")

    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
        conn.commit()

    return redirect("/admin/jobs")


# ==============================
# View Applications
# ==============================
@admin_bp.route("/applications")
def applications():

    if not admin_required():
        return redirect("/login")

    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        cur.execute("""
            SELECT id, user_id, job_id, status, applied_at
            FROM applications
            ORDER BY datetime(applied_at) DESC
        """)
        applications = cur.fetchall()

    return render_template("admin/applications.html", applications=applications)