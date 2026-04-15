import warnings
import pandas as pd
from src.config import SKILLS, SKILL_MATRIX_PATH
from src.data_loader import load_csv

def recommend_skills(data_path, user_skills, top_n=5):
    df = load_csv(data_path)

    available_skills = [s for s in SKILLS if s in df.columns]
    skill_matrix = df[available_skills]

    co_occurrence = skill_matrix.T.dot(skill_matrix)

    scores = {}

    for skill in user_skills:
        if skill not in co_occurrence.columns:
            warnings.warn(
                f"Skill '{skill}' not found in the skill matrix — skipping.",
                UserWarning,
                stacklevel=2,
            )
            continue

        related = co_occurrence[skill]

        for s in available_skills:
            if s not in user_skills:
                scores[s] = scores.get(s, 0) + related[s]

    recommendations = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return recommendations[:top_n]
