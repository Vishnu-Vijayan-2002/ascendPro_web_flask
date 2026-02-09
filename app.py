from flask import Flask, render_template
import sqlite3
from config import DATABASE

from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.applicant_routes import applicant_bp
from routes.company_routes import company_bp

app = Flask(__name__)
app.secret_key = "ascendpro_secret"

# ===============================
# CONTEXT PROCESSOR (IMPORTANT)
# ===============================
@app.context_processor
def inject_pending_count():
    try:
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM users WHERE approved = 0")
        pending_count = cur.fetchone()[0]
        conn.close()
    except Exception:
        pending_count = 0

    return dict(pending_count=pending_count)

# ===============================
# REGISTER BLUEPRINTS
# ===============================
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(applicant_bp, url_prefix="/applicant")
app.register_blueprint(company_bp, url_prefix="/company")

# ===============================
# HOME PAGE
# ===============================
@app.route("/")
def index():
    return render_template("index.html")

# ===============================
# RUN SERVER
# ===============================
if __name__ == "__main__":
    app.run(debug=True)
