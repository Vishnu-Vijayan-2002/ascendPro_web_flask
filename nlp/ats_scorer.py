import re

def calculate_ats_score(resume_text):
    """
    Calculate ATS (Applicant Tracking System) score for a resume
    Returns a score out of 100
    """
    score = 0
    max_score = 100
    feedback = []
    
    # Convert to lowercase for analysis
    text_lower = resume_text.lower()
    
    # 1. Check for Contact Information (15 points)
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    
    if re.search(email_pattern, resume_text):
        score += 8
    else:
        feedback.append("Add email address")
    
    if re.search(phone_pattern, resume_text):
        score += 7
    else:
        feedback.append("Add phone number")
    
    # 2. Check for Key Sections (25 points)
    sections = {
        'experience': ['experience', 'work history', 'employment', 'professional experience'],
        'education': ['education', 'academic', 'degree', 'university', 'college'],
        'skills': ['skills', 'technical skills', 'competencies', 'expertise'],
        'summary': ['summary', 'objective', 'profile', 'about']
    }
    
    for section_name, keywords in sections.items():
        if any(keyword in text_lower for keyword in keywords):
            score += 6
        else:
            feedback.append(f"Add {section_name} section")
    
    # 3. Skills Density (20 points)
    common_skills = [
        'python', 'java', 'javascript', 'c++', 'sql', 'react', 'node.js', 'django',
        'machine learning', 'data analysis', 'communication', 'leadership', 'teamwork',
        'project management', 'agile', 'scrum', 'git', 'aws', 'docker', 'kubernetes'
    ]
    
    skills_found = sum(1 for skill in common_skills if skill in text_lower)
    if skills_found >= 10:
        score += 20
    elif skills_found >= 5:
        score += 15
    elif skills_found >= 3:
        score += 10
    else:
        score += 5
        feedback.append("Add more relevant skills")
    
    # 4. Quantifiable Achievements (15 points)
    numbers_pattern = r'\d+%|\d+\+|increased|decreased|improved|reduced|generated|\$\d+'
    achievements = len(re.findall(numbers_pattern, text_lower))
    
    if achievements >= 5:
        score += 15
    elif achievements >= 3:
        score += 10
    elif achievements >= 1:
        score += 5
    else:
        feedback.append("Add quantifiable achievements (numbers, percentages)")
    
    # 5. Length Check (10 points)
    word_count = len(resume_text.split())
    if 300 <= word_count <= 800:
        score += 10
    elif 200 <= word_count <= 1000:
        score += 7
    else:
        feedback.append("Optimize resume length (300-800 words recommended)")
    
    # 6. Action Verbs (10 points)
    action_verbs = [
        'achieved', 'managed', 'led', 'developed', 'created', 'implemented',
        'designed', 'built', 'improved', 'increased', 'reduced', 'organized',
        'coordinated', 'executed', 'launched', 'delivered'
    ]
    
    verbs_found = sum(1 for verb in action_verbs if verb in text_lower)
    if verbs_found >= 5:
        score += 10
    elif verbs_found >= 3:
        score += 7
    elif verbs_found >= 1:
        score += 4
    else:
        feedback.append("Use more action verbs")
    
    # 7. No Common ATS Issues (5 points)
    # Check for tables, images, headers/footers issues (basic check)
    if not any(word in text_lower for word in ['table', 'image', 'graphic']):
        score += 5
    
    return min(score, max_score)  # Cap at 100