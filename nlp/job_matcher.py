from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def match_resume_with_jobs(resume_text, job_descriptions):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text] + job_descriptions)

    similarity_scores = cosine_similarity(vectors[0:1], vectors[1:])
    return similarity_scores[0]
