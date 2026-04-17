# 📄 AI Resume Analyzer & Job Matcher
🌐 **Live Demo:** https://resume-job-matcher-alpha.vercel.app/
---
⚙️ **Backend API:** https://resume-job-matcher-rajx.onrender.com
---
## 📌 Description:
A full-stack AI-powered web application that analyzes resumes against job descriptions and provides intelligent matching scores, skill insights, and job recommendations.
The system combines text analytics, intelligent scoring, and similarity algorithms to help users optimize their resumes for specific roles.
---
## 🚀 Features:
* 📊 **Resume Analysis** – Upload resume (PDF/Text) and compare with job description
* 🧠 **AI Similarity Score** – Calculates semantic similarity between resume and JD
* 📈 **Multi-Level Scoring System**
  * Analytics Score
  * Intelligence Score
  * AI Similarity Score
  * Final Combined Score
* 🧩 **Skill Matching**
  * Matched Skills
  * Missing Skills
  * Critical Skills
* 💡 **Smart Suggestions**
  * Resume improvement tips
  * Skill enhancement guidance
* 📉 **Skill Visualization**
  * Graphical representation of skill presence
* 💼 **Job Recommendations**
  * Fetches relevant jobs based on extracted skills
* 📁 **PDF Support**
  * Automatically extracts text from uploaded resumes
* 📊 **CSV Export**
  * Saves skill analysis data for external tools (e.g., Power BI)
---
## 🛠️ Tech Stack:
### Frontend:
* React.js
* Axios
* Recharts (for data visualization)
### Backend:
* Python (Flask)
* Pandas
* Scikit-learn (TF-IDF + Cosine Similarity)
* PyPDF2
### Deployment:
* Frontend → Vercel
* Backend → Render
---
## 📊 Workflow:
### 🔹 User Flow:
* Upload resume / paste text
* Enter job description
* Click analyze
* View:
  * Scores
  * Skill analysis
  * Suggestions
  * Job recommendations
---
### 🔹 System Flow:
* Frontend sends data → Flask API
* Backend:
  * Extracts text (PDF/Text)
  * Performs skill matching
  * Computes similarity scores
  * Generates insights
* Returns structured response → UI updates dynamically
---
## ⚙️ Getting Started:
### 🔹 Clone Repository:
```
git clone https://github.com/kavyasrinidhi/resume-job-matcher.git
cd resume-job-matcher
```
---
### 🔹 Backend Setup:
```
cd backend
pip install -r requirements.txt
python app.py
```
---
### 🔹 Frontend Setup:
```
cd frontend/src/resume-ui
npm install
npm start
```
---
## 🔐 Environment Variables:
Create `.env` in frontend:
```
REACT_APP_API_URL=https://resume-job-matcher-rajx.onrender.com
```
---
## ⚠️ Important Notes:
* Backend hosted on Render free tier → first request may take ~30 seconds
* Large AI models replaced with lightweight TF-IDF for optimized deployment
* Do not commit sensitive data (API keys, secrets)
---
## 🏷️ Summary:
A full-stack AI Resume Analyzer that evaluates resumes against job descriptions, provides actionable insights, and recommends jobs using intelligent scoring and text similarity techniques.
---
## 💼 Resume Highlight:
Developed and deployed a full-stack AI Resume Analyzer using React and Flask, enabling real-time resume evaluation, skill gap analysis, and job recommendations with optimized cloud deployment.
