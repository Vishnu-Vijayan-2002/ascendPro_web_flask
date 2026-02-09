import nltk
from nltk.tokenize import word_tokenize

def extract_skills(text):
    # fallback stopwords (manual)
    stop_words = {
        "and","or","the","is","to","in","of","for","with","a","an","on"
    }

    words = word_tokenize(text.lower())

    skill_set = [
        "python", "java", "sql", "flask", "django",
        "html", "css", "javascript",
        "machine learning", "ai"
    ]

    skills = [w for w in words if w in skill_set and w not in stop_words]
    return list(set(skills))
