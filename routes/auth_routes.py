from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from models.user_model import create_user, get_user

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.form

        create_user(
            data["name"],
            data["email"],
            data["password"],
            data["role"]
        )

        flash("Registration successful! Wait for admin approval.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = get_user(email, password)

        # 🚨 USER NOT FOUND
        if not user:
            flash("User not found or incorrect password.", "danger")
            return redirect(url_for("auth.login"))

        # Save session
        session["user_id"] = user["id"]
        session["role"] = user["role"]

        # 🔐 CHECK APPROVAL (for applicant & company)
        if user["role"] in ["applicant", "company"] and user["approved"] == 0:
            return redirect(url_for("auth.verification_pending"))

        # 🎯 ROLE BASED REDIRECT
        if user["role"] == "admin":
            return redirect("/admin/dashboard")

        if user["role"] == "applicant":
            return redirect("/applicant/dashboard")

        if user["role"] == "company":
            return redirect("/company/dashboard")

    return render_template("auth/login.html")
@auth_bp.route("/verification-pending")
def verification_pending():
    return render_template("auth/verification_pending.html")
