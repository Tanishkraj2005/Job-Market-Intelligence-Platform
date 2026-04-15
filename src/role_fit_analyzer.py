import pandas as pd
from src.config import SKILL_MATRIX_PATH, SKILLS
from src.data_loader import load_csv

def calculate_role_fit(current_skills, data_path=SKILL_MATRIX_PATH):
    try:
        df = load_csv(data_path)
    except FileNotFoundError:
        return {"error": "Data file not found."}

    if "Job Category" not in df.columns:
        return {"error": "'Job Category' column not found in data."}
    
    current_skills = set(s.lower() for s in current_skills)
    categories = df["Job Category"].unique()
    
    fit_scores = []
    
    for category in categories:
        if pd.isna(category) or category == "Other":
            continue
            
        cat_df = df[df["Job Category"] == category]
        if len(cat_df) == 0:
            continue
            
        skill_probs = {}
        for skill in SKILLS:
            if skill in cat_df.columns:
                skill_probs[skill] = cat_df[skill].mean()
                
        user_score = sum(prob for skill, prob in skill_probs.items() if skill in current_skills)
        
        top_skills = sorted(skill_probs.items(), key=lambda x: x[1], reverse=True)[:7]
        max_score = sum(prob for skill, prob in top_skills)
        
        if max_score > 0:
            fit_percentage = min((user_score / max_score) * 100, 100.0)
        else:
            fit_percentage = 0.0
            
        key_skills = [skill for skill, prob in top_skills if prob > 0.10]
        
        fit_scores.append({
            "role": category,
            "fit_score": round(fit_percentage, 1),
            "key_skills": key_skills
        })
        
    fit_scores = sorted(fit_scores, key=lambda x: x["fit_score"], reverse=True)
    
    return {
        "user_skills": list(current_skills),
        "role_fits": fit_scores
    }
