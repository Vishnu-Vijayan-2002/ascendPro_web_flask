from flask import Blueprint, request, render_template, redirect, url_for
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
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = get_user(
            request.form["email"],
            request.form["password"]
        )
        if user:
            if user[4] == "admin":
                return redirect("/admin/dashboard")
            if user[4] == "applicant":
                return redirect("/applicant/dashboard")
            if user[4] == "company":
                return redirect("/company/dashboard")
        return "Invalid login"
    return render_template("auth/login.html")
