import warnings
import pandas as pd
from src.config import SKILL_MATRIX_PATH, SKILLS
from src.data_loader import load_csv

def calculate_salary_gap(current_skills, target_salary, data_path=SKILL_MATRIX_PATH):
    try:
        df = load_csv(data_path)
    except FileNotFoundError:
        raise FileNotFoundError("Data file not found. Please run pipeline first.")
        
    df = df.dropna(subset=["salary_avg"])
    
    current_skills = [s.lower() for s in current_skills]
    
    mask_current = pd.Series(True, index=df.index)
    for skill in current_skills:
        if skill in df.columns:
            mask_current = mask_current & (df[skill] == 1)
            
    filtered_df = df[mask_current]
    
    if len(filtered_df) < 3:
        warnings.warn(
            "Fewer than 3 job postings matched your exact skill combination. "
            "Falling back to the overall market average for salary estimation.",
            UserWarning,
            stacklevel=2,
        )
        current_avg_salary = df["salary_avg"].mean()
        filtered_df = df
        mask_current = pd.Series(True, index=df.index)
    else:
        current_avg_salary = filtered_df["salary_avg"].mean()
    
    try:
        target_salary = float(target_salary)
        if target_salary >= 1000:
            target_salary = target_salary / 1000
    except ValueError:
        raise ValueError("Target salary must be a number.")

    salary_gap = target_salary - current_avg_salary

    if salary_gap <= 0:
         return {
            "current_salary": round(current_avg_salary, 1),
            "target_salary": target_salary,
            "gap": 0,
            "message": f"Your current skills place you at roughly ${current_avg_salary:.1f}K, which meets or exceeds your goal of ${target_salary}K!",
            "recommendations": []
        }
        
    missing_skills = [s for s in SKILLS if s not in current_skills and s in df.columns]
    
    recommendations = []
    
    for skill in missing_skills:
        mask_new = mask_current & (df[skill] == 1)
        skill_df = df[mask_new]
        
        if len(skill_df) >= 3:
            new_avg_salary = skill_df["salary_avg"].mean()
            if not pd.isna(new_avg_salary):
                boost = new_avg_salary - current_avg_salary
                if boost > 0:
                     recommendations.append({
                        "skill": skill,
                        "new_salary": new_avg_salary,
                        "boost": boost
                    })
    
    recommendations = sorted(recommendations, key=lambda x: x["boost"], reverse=True)
    
    best_recommendations = recommendations[:5]
    
    return {
        "current_salary": round(current_avg_salary, 1),
        "target_salary": target_salary,
        "gap": round(salary_gap, 1),
        "recommendations": best_recommendations
    }
