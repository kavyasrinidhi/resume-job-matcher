from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def compute_ai_similarity(resume_text, jd_text):
    vectorizer = TfidfVectorizer(stop_words='english')

    vectors = vectorizer.fit_transform([resume_text, jd_text])

    similarity = cosine_similarity(vectors[0], vectors[1])[0][0]

    return similarity * 100