from analytics_core import extract_skills
from intelligence_layer import apply_intelligence
from ai_enhancement import compute_ai_similarity

print("=== Resume Job Matcher ===\n")

# Take resume input
print("Paste Resume Text (Press Enter twice to finish):")
resume_lines = []
while True:
    line = input()
    if line == "":
        break
    resume_lines.append(line)

resume_text = "\n".join(resume_lines)

# Take JD input
print("\nPaste Job Description (Press Enter twice to finish):")
jd_lines = []
while True:
    line = input()
    if line == "":
        break
    jd_lines.append(line)

jd_text = "\n".join(jd_lines)

# Run Analytics Core
results = extract_skills(resume_text, jd_text)

# Run Intelligence Layer
intelligence = apply_intelligence(results)

# AI Enhancement
ai_score = compute_ai_similarity(resume_text, jd_text)
final_score = (0.7 * intelligence["weighted_match"]) + (0.3 * ai_score)

# Output
print("\n=== ANALYTICS RESULT ===")
print("Match %:", round(results["match_percentage"], 2))
print("Missing Skills:", results["missing_skills"])

print("\n=== INTELLIGENCE RESULT ===")
print("Weighted Match %:", round(intelligence["weighted_match"], 2))
print("High Priority Missing:", intelligence["high_priority_missing"])
print("Suggested Roles:", intelligence["suggested_roles"])


print("\n=== AI ENHANCEMENT ===")
print("AI Similarity Score:", round(ai_score, 2))

print("\n=== FINAL HYBRID SCORE ===")
print("Final Match Score:", round(final_score, 2))
