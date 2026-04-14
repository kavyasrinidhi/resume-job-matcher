def apply_intelligence(results):

    skills_df = results["skills_df"]
    resume_skills = results["resume_skills"]
    jd_skills = results["jd_skills"]
    missing_skills = results["missing_skills"]

    importance_map = dict(
        zip(
            skills_df["skill_name"].str.lower(),
            skills_df["importance"]
        )
    )

    weight_map = {
        "High": 3,
        "Medium": 2,
        "Low": 1
    }

    total_weight = 0
    matched_weight = 0

    for skill in jd_skills:

        importance = importance_map.get(skill, "Low")
        weight = weight_map.get(importance, 1)

        total_weight += weight

        if skill in resume_skills:
            matched_weight += weight

    if total_weight > 0:
        weighted_match = (matched_weight / total_weight) * 100
    else:
        weighted_match = 0

    high_priority_missing = [
        skill for skill in missing_skills
        if importance_map.get(skill) == "High"
    ]

    return {
        "weighted_match": weighted_match,
        "high_priority_missing": high_priority_missing
    }