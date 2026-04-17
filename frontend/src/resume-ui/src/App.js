import React, { useState, useEffect } from "react";
import { LabelList } from "recharts"; 
import axios from "axios";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  PieChart,
  Pie,
  Cell
} from "recharts";
import "./App.css";
// 🔹 Job List Component
const JobList = ({ jobs }) => {
  if (!jobs.length) {
    return <p>No jobs found 😢</p>;
  }

  return (
    <div style={{ display: "grid", gap: "15px" }}>
      {jobs.map((job, index) => (
        <div key={index} className="job-card">
          <h3>{job.title}</h3>
          <p><strong>Company:</strong> {job.company}</p>
          <p><strong>Location:</strong> {job.location}</p>

          <p>
            <strong>Match Score:</strong> {job.match_score}% 🎯
            {" "}
            {job.match_score >= 70 ? "🟢 High Match" :
            job.match_score >= 40 ? "🟡 Medium Match" :
            "🔴 Low Match"}
          </p>

          <a href={job.url} target="_blank" rel="noreferrer">
            <button style={styles.button} className="btn">Apply Now 🚀</button>
          </a>
        </div>
      ))}
    </div>
  );
};

const styles = {
  card: {
  padding: "20px",
  borderRadius: "16px",
  background: "#ffffff",
  color: "#1e293b",
  boxShadow: "0 10px 25px rgba(0,0,0,0.08)",
  border: "1px solid #e2e8f0",
  transition: "0.3s"
  },
  button: {
    marginTop: "10px",
    padding: "8px 12px",
    border: "none",
    borderRadius: "5px",
    backgroundColor: "#4CAF50",
    color: "white",
    cursor: "pointer"
  }
};
function App() {

  const [resumeText, setResumeText] = useState("");
  const [jdText, setJdText] = useState("");
  const [resumeFile, setResumeFile] = useState(null);
  const [jdFile, setJdFile] = useState(null);
  const [result, setResult] = useState(null);
  const [analyzeLoading, setAnalyzeLoading] = useState(false);
  const [jobLoading, setJobLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const [jobs, setJobs] = useState([]);
  const [skillData, setSkillData] = useState([]);
  const [message, setMessage] = useState("");
  // 🌙 Apply dark mode to FULL PAGE
  useEffect(() => {
    if (darkMode) {
      document.body.classList.add("dark");
    } else {
      document.body.classList.remove("dark");
    }
  }, [darkMode]);
  useEffect(() => {
    if (message) {
      const timer = setTimeout(() => {
        setMessage("");
      }, 3000); // disappears in 3 sec

      return () => clearTimeout(timer);
    }
  }, [message]);
  // 🔍 ANALYZE
  const handleAnalyze = async () => {

  if (!resumeText && !resumeFile) {
    setMessage("⚠️ Please upload or paste your Resume first!");
    return;
  }

  if (!jdText && !jdFile) {
    setMessage("⚠️ Please upload or paste Job Description!");
    return;
  }

  setMessage(""); // clear old message

  const formData = new FormData();

  if (resumeFile) formData.append("resume_file", resumeFile);
  else formData.append("resume_text", resumeText);

  if (jdFile) formData.append("jd_file", jdFile);
  else formData.append("jd_text", jdText);

  setAnalyzeLoading(true);
  setJobs([]);

  try {
    const res = await axios.post(`${process.env.REACT_APP_API_URL}/analyze`, formData);
    setResult(res.data);
    setSkillData(res.data.skill_analysis || []);
    setMessage("✅ Analysis completed successfully!");
  } catch (err) {
    console.error(err.response?.data || err.message);
    setMessage("❌ Server error. Please try again!");
  }

  setAnalyzeLoading(false);
};

  // 🔎 FETCH JOBS
  const fetchJobs = async () => {
  if (!result) return;

  setJobLoading(true); // 🔥 START loading

  try {
    const res = await axios.post(`${process.env.REACT_APP_API_URL}/jobs`, {
      skills: result.matched_skills
    });

    setJobs(res.data.data || []);
  } catch (err) {
    console.error(err);
    alert("Failed to fetch jobs");
  }

  setJobLoading(false); 
};
  const missingSkillsData = skillData
  .filter(s => s.user_has === "No")
  .map((s, index) => ({
    skill_name: s.skill_name,
    value: index + 1   
  }));
  return (
    <div className="container">
      {/* 🌙 Toggle */}
      <div className="toggle-container">
        <button 
          className="toggle-btn"
          onClick={() => setDarkMode(!darkMode)}
        >
          {darkMode ? "🌙" : "☀️"}
        </button>
      </div>

      <h1 id="home" className="title">AI Resume Matcher</h1>
      <div className="navbar">
      <button
        onClick={() => {
          document.getElementById("home")?.scrollIntoView({ behavior: "smooth" });
        }}
      >
        Home
      </button>

      <button
        onClick={() => {
          if (!result) {
            setMessage("⚠️ Please upload Resume & JD and click Analyze first!");
            return;
          }
          setMessage("");
          document.getElementById("score")?.scrollIntoView({ behavior: "smooth" });
        }}
      >
        Score
      </button>

      <button
        onClick={() => {
          if (!result) {
            setMessage("⚠️ Please analyze your resume before viewing jobs!");
            return;
          }
          setMessage("");
          document.getElementById("jobs")?.scrollIntoView({ behavior: "smooth" });
        }}
      >
        Jobs
      </button>
    </div>
    {message && (
      <div className="popup-message">
        {message}
      </div>
    )}
      {/* INPUT SECTION */}
      <div className="grid">

        {/* Resume */}
        <div className="card">
          <h3>Resume <h5>(.pdf)</h5>
            <span className="info-icon">
              ℹ️
              <span className="tooltip">
                Upload your resume in PDF or paste text. 
                Include skills, projects, and experience.
              </span>
            </span>
          </h3>

          <div className="file-upload">
            <label className="upload-btn">
              Upload Resume 📄
              <input
                type="file"
                accept=".pdf,.txt"
                onChange={(e) => setResumeFile(e.target.files[0])}
                hidden
              />
            </label>
          </div>

          {resumeFile ? (
            <div className="file-row">
              <p className="file-name">{resumeFile.name}</p>
              <span 
                className="remove-icon"
                onClick={() => setResumeFile(null)}
              >
                ❌
              </span>
            </div>
          ) : (
            <textarea
              placeholder="Or paste resume..."
              value={resumeText}
              onChange={(e) => setResumeText(e.target.value)}
            />
          )}
        </div>

        {/* JD */}
        <div className="card">
          <h3>Job Description <h5>(.pdf)</h5>
            <span className="info-icon">
              ℹ️
              <span className="tooltip">
                Paste a detailed job description. 
                Mention required skills like AWS, Python, etc.
              </span>
            </span>
          </h3>

          <div className="file-upload">
            <label className="upload-btn">
              Upload JD 📋
              <input
                type="file"
                accept=".pdf,.txt"
                onChange={(e) => setJdFile(e.target.files[0])}
                hidden
              />
            </label>
          </div>

          {jdFile ? (
            <div className="file-row">
              <p className="file-name">{jdFile.name}</p>
              <span 
                className="remove-icon"
                onClick={() => setJdFile(null)}
              >
                ❌
              </span>
            </div>
          ) : (
            <textarea
              placeholder="Or paste job description..."
              value={jdText}
              onChange={(e) => setJdText(e.target.value)}
            />
          )}
        </div>
      </div>

      {/* ANALYZE BUTTON */}
      <button className="btn" onClick={handleAnalyze}>
        {analyzeLoading  ? "Analyzing..." : "Analyze 🚀"}
      </button>

      {/* RESULT */}
      {result && (
        <div id="score" className="result">

          <h2 className="result-title">Match Score: {result.final_score}%</h2>

          {/* 📊 DASHBOARD */}
          <div className="dashboard-section">

            <h2>📊 Skill Gap Dashboard</h2>

            <div className="charts-grid">

              <div className="chart-card">
                <h3>Missing Skills</h3>
                <BarChart width={400} height={300} data={missingSkillsData}>
                  <XAxis 
                    dataKey="skill_name" 
                    angle={-30} 
                    textAnchor="end" 
                    interval={0}
                  />
                  <YAxis />
                  <Tooltip />

                  <Bar dataKey="value" fill="#ef4444">
                    <LabelList 
                      dataKey="skill_name" 
                      position="insideTop" 
                      style={{ fill: "#fff", fontSize: "10px" }} 
                    />
                  </Bar>
                </BarChart>
              </div>

              <div className="chart-card">
                <h3>Skill Availability</h3>
                <PieChart width={300} height={250}>
                  <Pie
                    data={[
                      { name: "Present", value: skillData.filter(s => s.user_has === "Yes").length },
                      { name: "Missing", value: skillData.filter(s => s.user_has === "No").length }
                    ]}
                    dataKey="value"
                    outerRadius={80}
                    label
                  >
                    <Cell fill="#22c55e" />
                    <Cell fill="#ef4444" />
                  </Pie>
                  <Tooltip />
                </PieChart>
              </div>

            </div>
          </div>
          <h3>🧠 Resume Improvement Suggestions</h3>
          <div className="suggestions">
            {result.suggestions?.map((s, i) => (
              <p style={{ textAlign: "justify"}} key={i}>📌 {s}</p>
            ))}
          </div>
          {/* SKILLS */}
          <h3>Matched Skills</h3>
          <div className="tags">
            {result.matched_skills.map((s, i) => (
              <span key={i}>{s}</span>
            ))}
          </div>

          <h3>Missing Skills</h3>
          <div className="tags">
            {result.missing_skills.length
              ? result.missing_skills.map((s, i) => (
                  <span key={i}>{s}</span>
                ))
              : <span>None</span>}
          </div>

          {/* 🔍 FIND JOBS */}
          <button className="btn" onClick={fetchJobs} disabled={jobLoading }>
            {jobLoading ? "Finding..." : "Find Jobs 🔍"}
          </button>
        </div>
      )}
      <div className="dashboard-section">

    </div>
      {/* JOB RESULTS */}
      {jobs.length > 0 && (
        <div id="jobs" className="jobs-section">
          <h2>🚀 Recommended Jobs</h2>
          <JobList jobs={jobs} />
        </div>
      )}

    </div>
    
  );
}

export default App;