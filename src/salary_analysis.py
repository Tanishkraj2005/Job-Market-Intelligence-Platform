import pandas as pd
from src.config import SKILLS, SKILL_MATRIX_PATH
from src.data_loader import load_csv

def salary_by_skill(data_path=SKILL_MATRIX_PATH):

    df = load_csv(data_path)
    
    if "salary_avg" not in df.columns:
        return pd.DataFrame(columns=["Average Salary"])

    salary_dict = {}

    for skill in SKILLS:
        salary_dict[skill] = df[df[skill] == 1]["salary_avg"].mean()

    return pd.DataFrame.from_dict(
        salary_dict,
        orient="index",
        columns=["Average Salary"]
    )

def salary_by_skill_for_role(job_category, data_path=SKILL_MATRIX_PATH):
    df = load_csv(data_path)

    if "Job Category" in df.columns and job_category:
        df = df[df["Job Category"] == job_category]

    if df.empty or "salary_avg" not in df.columns:
        return pd.DataFrame(columns=["Average Salary"])

    df = df.dropna(subset=["salary_avg"])

    salary_dict = {}
    available_skills = [s for s in SKILLS if s in df.columns]
    for skill in available_skills:
        mean_val = df[df[skill] == 1]["salary_avg"].mean()
        if not pd.isna(mean_val):
            salary_dict[skill] = mean_val

    return pd.DataFrame.from_dict(salary_dict, orient="index", columns=["Average Salary"])
