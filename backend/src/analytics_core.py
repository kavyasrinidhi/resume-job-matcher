import pandas as pd
import os
from rapidfuzz import fuzz
from src.preprocessing import preprocess_text


def fuzzy_match(skill, tokens):

    for token in tokens:

        if fuzz.partial_ratio(skill, token) > 85:
            return True

    return False


def extract_skills(resume_text, jd_text):

    resume_words, resume_ngrams = preprocess_text(resume_text)
    jd_words, jd_ngrams = preprocess_text(jd_text)

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    skills_path = os.path.join(BASE_DIR, "data", "skills.csv")

    skills_df = pd.read_csv(skills_path)
    skills_list = skills_df["skill_name"].str.lower().tolist()

    resume_skills = set()
    jd_skills = set()

    for skill in skills_list:

        if skill in resume_ngrams or fuzzy_match(skill, resume_ngrams):
            resume_skills.add(skill)

        if skill in jd_ngrams or fuzzy_match(skill, jd_ngrams):
            jd_skills.add(skill)

    matched_skills = resume_skills & jd_skills
    missing_skills = jd_skills - resume_skills

    if len(jd_skills) > 0:
        match_percentage = (len(matched_skills) / len(jd_skills)) * 100
    else:
        match_percentage = 0

    return {
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_percentage": match_percentage,
        "skills_df": skills_df
    }