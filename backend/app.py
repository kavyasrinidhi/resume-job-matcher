import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from flask import Flask, request, jsonify
import PyPDF2
import io
import requests
from flask_cors import CORS
import pandas as pd


# Your modules
from analytics_core import extract_skills
from intelligence_layer import apply_intelligence
from ai_enhancement import compute_ai_similarity
from final_scoring import compute_final_score

app = Flask(__name__)
CORS(app)

print("🚀 Flask App Started")


# ----------------------------------------
# HOME ROUTE
# ----------------------------------------
@app.route('/')
def home():
    return jsonify({"message": "✅ Resume Matcher API is running"})


# ----------------------------------------
# PDF TEXT EXTRACTOR
# ----------------------------------------
def extract_pdf_text(file_bytes):
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text = ""

        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

        return text.strip()

    except Exception as e:
        print("PDF Error:", e)
        return ""


# ----------------------------------------
# ANALYZE RESUME + JD
# ----------------------------------------
@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        resume_text = request.form.get('resume_text', "")
        jd_text = request.form.get('jd_text', "")

        # -------- FILE HANDLING --------
        if 'resume_file' in request.files:
            file = request.files['resume_file']
            if file.filename:
                if file.filename.endswith('.pdf'):
                    resume_text = extract_pdf_text(file.read())
                else:
                    resume_text = file.read().decode("utf-8", errors="ignore")

        if 'jd_file' in request.files:
            file = request.files['jd_file']
            if file.filename:
                if file.filename.endswith('.pdf'):
                    jd_text = extract_pdf_text(file.read())
                else:
                    jd_text = file.read().decode("utf-8", errors="ignore")

        if not resume_text or not jd_text:
            return jsonify({"error": "❌ Missing resume or job description"}), 400

        # -------- EXISTING LOGIC --------
        results = extract_skills(resume_text, jd_text)
        intelligence = apply_intelligence(results)
        ai_score = float(compute_ai_similarity(resume_text, jd_text))

        analytics_score = float(results.get("match_percentage", 0))
        intelligence_score = float(intelligence.get("weighted_match", 0))

        final_score = compute_final_score(
            analytics_score,
            intelligence_score,
            ai_score
        )

        # ----------------------------------------
        # 🔥 CREATE DASHBOARD DATA
        # ----------------------------------------

        matched = list(results.get("matched_skills", []))
        missing = list(results.get("missing_skills", []))
        suggestions = []

        if missing:
            suggestions.append(f"Add these skills to your resume: {', '.join(missing[:5])}")

        suggestions.append("Update your resume summary to match the job role.")

        suggestions.append("Include projects using technologies mentioned in the job description.")

        suggestions.append("Use action verbs and quantify your achievements (e.g., improved performance by 30%).")

        suggestions.append("Align your resume keywords with the job description for better matching.")

        all_skills = list(set(matched + missing))

        skill_analysis = []

        for skill in all_skills:
            skill_analysis.append({
                "skill_name": skill,
                "user_has": "Yes" if skill in matched else "No"
            })

        # ----------------------------------------
        # 🔥 SAVE CSV (for Power BI / backup)
        # ----------------------------------------

        df = pd.DataFrame(skill_analysis)

        os.makedirs("data", exist_ok=True)

        base_dir = os.path.dirname(os.path.abspath(__file__))

        data_dir = os.path.join(base_dir, "data")
        os.makedirs(data_dir, exist_ok=True)

        file_path = os.path.join(data_dir, "user_skill_analysis.csv")
        df.to_csv(file_path, index=False)

        print("✅ CSV saved at:", file_path)

        # ----------------------------------------

        return jsonify({
            "final_score": round(final_score, 2),
            "analytics_score": round(analytics_score, 2),
            "intelligence_score": round(intelligence_score, 2),
            "ai_score": round(ai_score, 2),
            "matched_skills": matched,
            "missing_skills": missing,
            "critical_skills": list(intelligence.get("high_priority_missing", [])),
            "skill_analysis": skill_analysis,
            "suggestions": suggestions
        })

    except Exception as e:
        return jsonify({
            "error": "❌ Server error",
            "details": str(e)
        }), 500


# ----------------------------------------
# JOB MATCH SCORE FUNCTION 🧠
# ----------------------------------------
def calculate_match_score(job, skills):
    text = (job.get("title", "") + job.get("description", "")).lower()

    match_count = sum(
        1 for skill in skills if skill.lower() in text
    )

    return round((match_count / len(skills)) * 100, 2) if skills else 0


# ----------------------------------------
# JOB SEARCH (MULTI-QUERY 🔥)
# ----------------------------------------
@app.route('/jobs', methods=['POST'])
def get_jobs():
    try:
        data = request.json
        skills = data.get("skills", [])

        if not skills:
            return jsonify({"data": []})

        queries = skills[:3]
        all_jobs = []

        for q in queries:
            url = f"https://remotive.com/api/remote-jobs?search={q}"
            response = requests.get(url)

            if response.status_code == 200:
                jobs = response.json().get("jobs", [])
                all_jobs.extend(jobs)

        # Remove duplicates
        unique_jobs = {}
        for job in all_jobs:
            job_id = job.get("id")
            if job_id not in unique_jobs:
                unique_jobs[job_id] = job

        jobs = list(unique_jobs.values())

        if not jobs:
            response = requests.get("https://remotive.com/api/remote-jobs?search=developer")
            jobs = response.json().get("jobs", [])

        formatted_jobs = []

        for job in jobs:
            score = calculate_match_score(job, skills)

            formatted_jobs.append({
                "title": job.get("title"),
                "company": job.get("company_name"),
                "location": job.get("candidate_required_location"),
                "url": job.get("url"),
                "match_score": score
            })

        formatted_jobs = sorted(
            formatted_jobs,
            key=lambda x: x["match_score"],
            reverse=True
        )

        return jsonify({"data": formatted_jobs[:10]})

    except Exception as e:
        return jsonify({
            "error": "❌ Job API error",
            "details": str(e)
        }), 500


# ----------------------------------------
# RUN SERVER
# ----------------------------------------
if __name__ == '__main__':
    print("✅ All imports successful")
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)