from flask import Blueprint, render_template, request, redirect, make_response, send_file
import sqlite3
from config import DATABASE
from nlp.skill_extractor import extract_skills   # NLP
from nlp.ats_scorer import calculate_ats_score   # ATS Scorer
from werkzeug.utils import secure_filename
import PyPDF2
import docx
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io
import os
from datetime import datetime

applicant_bp = Blueprint("applicant", __name__)

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(file):
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return ""

def extract_text_from_docx(file):
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(file)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text.strip()
    except Exception as e:
        print(f"Error extracting DOCX: {e}")
        return ""

def extract_text_from_txt(file):
    """Extract text from TXT file"""
    try:
        return file.read().decode('utf-8').strip()
    except Exception as e:
        print(f"Error extracting TXT: {e}")
        return ""

# Dashboard
@applicant_bp.route("/dashboard")
def dashboard():
    return render_template("applicant/dashboard.html")

# Upload Resume + NLP + ATS Score
@applicant_bp.route("/upload-resume", methods=["GET", "POST"])
def upload_resume():
    message = ""
    skills = []
    ats_score = None

    if request.method == "POST":
        user_id = request.form.get("user_id")
        content = ""
        
        # Check if file was uploaded
        if 'resume' in request.files:
            file = request.files['resume']
            
            # Check if file is selected
            if file.filename == '':
                message = "⚠️ No file selected"
                return render_template(
                    "applicant/upload_resume.html",
                    message=message,
                    skills=skills,
                    ats_score=ats_score
                )
            
            # Validate and process file
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_ext = filename.rsplit('.', 1)[1].lower()
                
                # Reset file pointer to beginning
                file.stream.seek(0)
                
                # Extract text based on file type
                if file_ext == 'pdf':
                    content = extract_text_from_pdf(file)
                elif file_ext == 'docx':
                    content = extract_text_from_docx(file)
                elif file_ext == 'txt':
                    content = extract_text_from_txt(file)
                
                # Check if text extraction was successful
                if not content or len(content.strip()) < 10:
                    message = "⚠️ Could not extract text from file. Please try another format or check the file content."
                    return render_template(
                        "applicant/upload_resume.html",
                        message=message,
                        skills=skills,
                        ats_score=ats_score
                    )
            else:
                message = "⚠️ Invalid file format. Please upload PDF, DOCX, or TXT"
                return render_template(
                    "applicant/upload_resume.html",
                    message=message,
                    skills=skills,
                    ats_score=ats_score
                )
        else:
            message = "⚠️ No file uploaded"
            return render_template(
                "applicant/upload_resume.html",
                message=message,
                skills=skills,
                ats_score=ats_score
            )

        # NLP skill extraction
        skills = extract_skills(content)
        
        # Calculate ATS Score
        ats_score = calculate_ats_score(content)

        # Save to database
        try:
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()

            cur.execute(
                "INSERT INTO resumes (user_id, content, ats_score) VALUES (?, ?, ?)",
                (user_id, content, ats_score)
            )

            conn.commit()
            conn.close()

            message = "✅ Resume uploaded successfully!"
        except Exception as e:
            message = f"⚠️ Database error: {str(e)}"
            print(f"Database error: {e}")

    return render_template(
        "applicant/upload_resume.html",
        message=message,
        skills=skills,
        ats_score=ats_score
    )

# Build Resume
@applicant_bp.route("/build-resume", methods=["GET", "POST"])
def build_resume():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        
        # Collect all form data
        resume_data = collect_resume_data(request.form)
        
        # Generate resume content
        content = generate_professional_resume(resume_data)
        
        # Calculate ATS Score
        ats_score = calculate_ats_score(content)
        skills = extract_skills(content)
        
        # Save to database
        try:
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            
            cur.execute(
                "INSERT INTO resumes (user_id, content, ats_score) VALUES (?, ?, ?)",
                (user_id, content, ats_score)
            )
            
            resume_id = cur.lastrowid
            
            conn.commit()
            conn.close()
            
            return render_template(
                "applicant/resume_preview.html",
                resume_id=resume_id,
                user_id=user_id,
                content=content,
                ats_score=ats_score,
                skills=skills,
                resume_data=resume_data,
                message="✅ Professional resume created successfully!"
            )
        except Exception as e:
            print(f"Database error: {e}")
            return render_template(
                "applicant/build_resume.html",
                error=f"⚠️ Error saving resume: {str(e)}"
            )
    
    return render_template("applicant/build_resume.html")

# Edit Resume
@applicant_bp.route("/edit-resume/<int:resume_id>", methods=["GET", "POST"])
def edit_resume(resume_id):
    if request.method == "POST":
        user_id = request.form.get("user_id")
        
        # Collect all form data
        resume_data = collect_resume_data(request.form)
        
        # Generate resume content
        content = generate_professional_resume(resume_data)
        
        # Calculate ATS Score
        ats_score = calculate_ats_score(content)
        skills = extract_skills(content)
        
        # Update database
        try:
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            
            cur.execute(
                "UPDATE resumes SET content = ?, ats_score = ? WHERE id = ?",
                (content, ats_score, resume_id)
            )
            
            conn.commit()
            conn.close()
            
            return render_template(
                "applicant/resume_preview.html",
                resume_id=resume_id,
                user_id=user_id,
                content=content,
                ats_score=ats_score,
                skills=skills,
                resume_data=resume_data,
                message="✅ Resume updated successfully!"
            )
        except Exception as e:
            print(f"Database error: {e}")
            return render_template(
                "applicant/build_resume.html",
                error=f"⚠️ Error updating resume: {str(e)}"
            )
    
    # GET request - load existing resume
    try:
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("SELECT content, user_id FROM resumes WHERE id = ?", (resume_id,))
        result = cur.fetchone()
        conn.close()
        
        if result:
            content, user_id = result
            # You'd need to parse the content back to form data
            # For now, redirect to build page
            return render_template("applicant/build_resume.html")
        else:
            return redirect("/applicant/dashboard")
    except Exception as e:
        print(f"Error: {e}")
        return redirect("/applicant/dashboard")

# Download Resume as DOCX
@applicant_bp.route("/download-resume/<int:resume_id>")
def download_resume(resume_id):
    try:
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("SELECT content, user_id FROM resumes WHERE id = ?", (resume_id,))
        result = cur.fetchone()
        conn.close()
        
        if not result:
            return "Resume not found", 404
        
        content, user_id = result
        
        # Create DOCX file
        doc = create_professional_docx(content)
        
        # Save to BytesIO
        file_stream = io.BytesIO()
        doc.save(file_stream)
        file_stream.seek(0)
        
        # Create filename
        filename = f"Resume_{user_id}_{datetime.now().strftime('%Y%m%d')}.docx"
        
        return send_file(
            file_stream,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
    except Exception as e:
        print(f"Download error: {e}")
        return f"Error downloading resume: {str(e)}", 500

def collect_resume_data(form):
    """Collect all form data into a dictionary"""
    data = {
        'full_name': form.get('full_name'),
        'location': form.get('location'),
        'phone': form.get('phone'),
        'email': form.get('email'),
        'linkedin': form.get('linkedin', ''),
        'github': form.get('github', ''),
        'portfolio': form.get('portfolio', ''),
        'summary': form.get('summary'),
        'skills_languages': form.get('skills_languages', ''),
        'skills_frontend': form.get('skills_frontend', ''),
        'skills_backend': form.get('skills_backend', ''),
        'skills_database': form.get('skills_database', ''),
        'skills_tools': form.get('skills_tools', ''),
        'educations': [],
        'projects': [],
        'experiences': [],
        'certifications': []
    }
    
    # Education
    edu_count = int(form.get('education_count', 0))
    for i in range(edu_count):
        edu = {
            'degree': form.get(f'edu_degree_{i}'),
            'institution': form.get(f'edu_institution_{i}'),
            'duration': form.get(f'edu_duration_{i}'),
            'details': form.get(f'edu_details_{i}', '')
        }
        data['educations'].append(edu)
    
    # Projects
    proj_count = int(form.get('projects_count', 0))
    for i in range(proj_count):
        proj = {
            'name': form.get(f'project_name_{i}'),
            'date': form.get(f'project_date_{i}', ''),
            'github': form.get(f'project_github_{i}', ''),
            'live': form.get(f'project_live_{i}', ''),
            'description': form.get(f'project_description_{i}'),
            'tech': form.get(f'project_tech_{i}')
        }
        data['projects'].append(proj)
    
    # Experience
    exp_count = int(form.get('experience_count', 0))
    for i in range(exp_count):
        exp = {
            'title': form.get(f'exp_title_{i}'),
            'company': form.get(f'exp_company_{i}'),
            'location': form.get(f'exp_location_{i}', ''),
            'duration': form.get(f'exp_duration_{i}'),
            'description': form.get(f'exp_description_{i}')
        }
        data['experiences'].append(exp)
    
    # Certifications
    cert_count = int(form.get('certifications_count', 0))
    for i in range(cert_count):
        cert = {
            'name': form.get(f'cert_name_{i}'),
            'org': form.get(f'cert_org_{i}'),
            'date': form.get(f'cert_date_{i}', ''),
            'credential': form.get(f'cert_credential_{i}', ''),
            'description': form.get(f'cert_description_{i}', '')
        }
        data['certifications'].append(cert)
    
    return data

def generate_professional_resume(data):
    """Generate professional ATS-friendly resume content"""
    
    # Header
    content = f"{data['full_name']}\n"
    links = []
    if data['linkedin']:
        links.append(f"LinkedIn: {data['linkedin']}")
    if data['github']:
        links.append(f"GitHub: {data['github']}")
    if data['portfolio']:
        links.append(f"Portfolio: {data['portfolio']}")
    
    content += f"{data['location']} | {data['phone']} | {data['email']}"
    if links:
        content += " | " + " | ".join(links)
    content += "\n\n"
    
    # Professional Summary
    if data['summary']:
        content += "Professional Summary\n"
        content += f"{data['summary']}\n\n"
    
    # Education
    if data['educations']:
        content += "Education\n"
        for edu in data['educations']:
            if edu['degree'] and edu['institution']:
                content += f"{edu['degree']}\n"
                content += f"{edu['institution']}"
                if edu['duration']:
                    content += f" | {edu['duration']}"
                content += "\n"
                if edu['details']:
                    content += f"{edu['details']}\n"
                content += "\n"
    
    # Technical Skills
    content += "Technical Skills\n"
    if data['skills_languages']:
        content += f"Languages: {data['skills_languages']}\n"
    if data['skills_frontend']:
        content += f"Frontend: {data['skills_frontend']}\n"
    if data['skills_backend']:
        content += f"Backend: {data['skills_backend']}\n"
    if data['skills_database']:
        content += f"Database: {data['skills_database']}\n"
    if data['skills_tools']:
        content += f"Tools: {data['skills_tools']}\n"
    content += "\n"
    
    # Projects
    if data['projects']:
        content += "Projects\n"
        for proj in data['projects']:
            if proj['name']:
                proj_links = []
                if proj['github']:
                    proj_links.append(f"GitHub: {proj['github']}")
                if proj['live']:
                    proj_links.append(f"Live: {proj['live']}")
                
                content += f"{proj['name']}"
                if proj_links:
                    content += f" | {' | '.join(proj_links)}"
                if proj['date']:
                    content += f" | {proj['date']}"
                content += "\n"
                
                if proj['description']:
                    content += f"{proj['description']}\n"
                if proj['tech']:
                    content += f"Tech Stack: {proj['tech']}\n"
                content += "\n"
    
    # Professional Experience
    if data['experiences']:
        content += "Professional Experience\n"
        for exp in data['experiences']:
            if exp['title'] and exp['company']:
                content += f"{exp['title']} | {exp['company']}"
                if exp['location']:
                    content += f" | {exp['location']}"
                content += "\n"
                if exp['duration']:
                    content += f"{exp['duration']}\n"
                if exp['description']:
                    content += f"{exp['description']}\n"
                content += "\n"
    
    # Certifications
    if data['certifications']:
        content += "Certifications\n"
        for cert in data['certifications']:
            if cert['name'] and cert['org']:
                content += f"{cert['name']} – {cert['org']}"
                if cert['date']:
                    content += f" | {cert['date']}"
                content += "\n"
                if cert['description']:
                    content += f"{cert['description']}\n"
                if cert['credential']:
                    content += f"Credential: {cert['credential']}\n"
                content += "\n"
    
    return content

def create_professional_docx(content):
    """Create a professional formatted DOCX from resume content"""
    doc = Document()
    
    # Set margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)
    
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        
        # Name (first line) - Large, bold, centered
        if i == 0:
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(line)
            run.font.size = Pt(18)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0, 0, 0)
            
        # Contact info (second line) - Centered
        elif i == 1:
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(line)
            run.font.size = Pt(10)
            
        # Section headings (Professional Summary, Education, etc.)
        elif line in ['Professional Summary', 'Education', 'Technical Skills', 'Projects', 
                     'Professional Experience', 'Certifications']:
            p = doc.add_paragraph()
            run = p.add_run(line.upper())
            run.font.size = Pt(12)
            run.font.bold = True
            run.font.color.rgb = RGBColor(31, 78, 121)
            # Add bottom border
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(6)
            
        # Bullet points
        elif line.strip().startswith('•') or line.strip().startswith('-'):
            p = doc.add_paragraph(line.strip(), style='List Bullet')
            p.paragraph_format.left_indent = Inches(0.25)
            run = p.runs[0]
            run.font.size = Pt(10)
            
        # Regular content
        else:
            p = doc.add_paragraph(line)
            run = p.runs[0] if p.runs else p.add_run(line)
            run.font.size = Pt(10)
    
    return doc

# View Jobs
@applicant_bp.route("/jobs")
def jobs():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM jobs")
    jobs = cur.fetchall()
    conn.close()
    return render_template("applicant/job_list.html", jobs=jobs)

# Apply Job
@applicant_bp.route("/apply/<int:job_id>/<int:user_id>")
def apply(job_id, user_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO applications (user_id, job_id, status) VALUES (?, ?, ?)",
        (user_id, job_id, "Applied")
    )

    cur.execute(
        "INSERT INTO notifications (user_id, message) VALUES (?, ?)",
        (user_id, "📩 Application submitted successfully")
    )

    conn.commit()
    conn.close()

    return redirect("/applicant/jobs")