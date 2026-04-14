from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import streamlit as st


@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


def compute_ai_similarity(resume_text, jd_text):

    model = load_model()

    resume_sentences = resume_text.split(".")
    jd_sentences = jd_text.split(".")

    resume_emb = model.encode(resume_sentences)
    jd_emb = model.encode(jd_sentences)

    similarity_matrix = cosine_similarity(resume_emb, jd_emb)

    score = np.mean(similarity_matrix)

    return score * 100