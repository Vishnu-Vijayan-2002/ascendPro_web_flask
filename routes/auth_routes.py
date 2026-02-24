from flask import Blueprint, request, render_template, redirect, url_for, flash, session
import sqlite3
from config import DATABASE
from models.user_model import create_user, get_user
from functools import wraps

auth_bp = Blueprint("auth", __name__)


# ======================================
# ROUTE GUARDS
# ======================================
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


def role_required(*roles):
    """Usage: @role_required('admin') or @role_required('admin', 'company')"""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if "user_id" not in session:
                flash("Please log in to continue.", "warning")
                return redirect(url_for("auth.login"))
            if session.get("role") not in roles:
                flash("You do not have permission to access that page.", "danger")
                return redirect(url_for("auth.login"))
            return f(*args, **kwargs)
        return decorated
    return decorator


# ======================================
# HELPERS
# ======================================
def _redirect_by_role(role):
    routes = {
        "admin":     "/admin/dashboard",
        "company":   "/company/dashboard",
        "applicant": "/applicant/dashboard",
    }
    return redirect(routes.get(role, "/login"))


def _load_company_session(user_id):
    """Load company_details into session if available."""
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM company_details WHERE user_id = ?", (user_id,))
        details = cur.fetchone()
        if details:
            session["company_name"] = details["company_name"]
            session["verified"]     = details["verified"]
        else:
            session["company_name"] = session.get("name", "")
            session["verified"]     = 0


# ======================================
# REGISTER
# ======================================
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    # Already logged in → go to dashboard
    if "user_id" in session:
        return _redirect_by_role(session.get("role"))

    if request.method == "POST":
        name     = request.form.get("name", "").strip()
        email    = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        role     = request.form.get("role", "").strip()

        # Basic validation
        if not all([name, email, password, role]):
            flash("All fields are required.", "danger")
            return redirect(url_for("auth.register"))

        if role not in ("company", "applicant"):
            flash("Invalid role selected.", "danger")
            return redirect(url_for("auth.register"))

        create_user(name, email, password, role)
        flash("Registration successful! Wait for admin approval.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


# ======================================
# LOGIN
# ======================================
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # Already logged in → go to dashboard
    if "user_id" in session:
        return _redirect_by_role(session.get("role"))

    if request.method == "POST":
        email    = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        # Basic validation
        if not email or not password:
            flash("Email and password are required.", "danger")
            return redirect(url_for("auth.login"))

        user = get_user(email, password)

        if not user:
            flash("Invalid email or password.", "danger")
            return redirect(url_for("auth.login"))

        if user["approved"] == 0:
            return redirect(url_for("auth.verification_pending"))

        # Build session
        session.clear()
        session["user_id"] = user["id"]
        session["role"]    = user["role"]
        session["name"]    = user["name"]

        # Load extra details for company accounts
        if user["role"] == "company":
            _load_company_session(user["id"])

        return _redirect_by_role(user["role"])

    return render_template("auth/login.html")


# ======================================
# VERIFICATION PENDING PAGE
# ======================================
@auth_bp.route("/verification-pending")
def verification_pending():
    return render_template("auth/verification_pending.html")


# ======================================
# LOGOUT
# ======================================
@auth_bp.route("/logout")
@login_required
def logout():
    session.clear()
    flash("You have been logged out successfully.", "info")
    return redirect(url_for("auth.login"))