🚀 AscendPro – Smart Placement & Recruitment System

AscendPro is a web-based smart placement platform built using Flask, SQLite, HTML, CSS, and AI/NLP concepts.
It connects Applicants, Companies, and Admins on a single platform to make recruitment efficient, transparent, and intelligent.

📌 Project Objectives

Automate placement and recruitment processes

Enable resume upload and analysis

Provide AI-based job matching

Allow companies to manage job postings and applicants

Give admin full control and monitoring capability

🧠 Key Features
👨‍💼 Admin Module

Approve applicant and company registrations

Monitor job postings

View and manage pending users

Dashboard with real-time pending user count

System-level control and transparency

👤 Applicant Module

User registration and login

Resume upload (text-based)

NLP-based skill extraction

View available job listings

Apply for jobs

Receive application notifications

🏢 Company Module

Company registration and login

Post and manage job vacancies

View applicant profiles

Shortlist applicants

Send notifications to candidates

🤖 AI & NLP Features

Resume text analysis

Skill extraction using keyword matching (NLP concept)

Foundation for AI-based job recommendation

Demonstrates practical AI usage suitable for academic projects

🛠️ Technology Stack
Layer	Technology
Backend	Python, Flask
Frontend	HTML, CSS, JavaScript
Database	SQLite
AI/NLP	Resume parsing, skill extraction
Architecture	MVC (Model–View–Controller)
📂 Project Structure
AscendPro/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
│
├── database/
│   └── ascendpro.db
│
├── models/
│   ├── user_model.py
│   ├── job_model.py
│   ├── application_model.py
│   └── resume_model.py
│
├── routes/
│   ├── auth_routes.py
│   ├── admin_routes.py
│   ├── applicant_routes.py
│   └── company_routes.py
│
├── nlp/
│   └── skill_extractor.py
│
├── static/
│   ├── css/
│   ├── js/
│   └── admin/
│
├── templates/
│   ├── admin/
│   ├── applicant/
│   ├── company/
│   └── auth/
│
└── venv/

⚙️ Installation & Setup
1️⃣ Clone / Download Project
git clone <repository-url>
cd AscendPro

2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows

3️⃣ Install Dependencies
pip install flask

4️⃣ Run the Application
python app.py

5️⃣ Open in Browser
http://127.0.0.1:5000/

🔐 Default Roles

Admin – Full system access

Applicant – Job seeker

Company – Recruiter

(Admin approval required for new users)

📊 Database Tables

users

jobs

applications

resumes

notifications
