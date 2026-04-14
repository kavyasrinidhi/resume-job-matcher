def compute_final_score(analytics_score, intelligence_score, ai_score):

    final_score = (
        0.4 * analytics_score
        + 0.35 * intelligence_score
        + 0.25 * ai_score
    )

    return final_score