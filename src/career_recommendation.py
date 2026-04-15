import pandas as pd
from src.config import SKILLS, SKILL_MATRIX_PATH
from src.data_loader import load_csv

ROLE_CATEGORY_MAP = {
    "Data Analyst": "Data Analyst (General)",
    "Data Scientist": "Data Scientist",
    "Data Engineer": "Data Engineer",
    "Business Analyst": "Business Analyst",
    "Senior Analyst": "Senior Analyst",
    "Junior Analyst": "Junior Analyst",
    "Technical Analyst": "Technical Analyst"
}

def career_skill_gap(data_path, user_skills, role, skill_matrix_path=SKILL_MATRIX_PATH):
    try:
        df = load_csv(skill_matrix_path)
    except FileNotFoundError:
        return {"error": "Skill matrix not found. Please run the pipeline first."}

    category = ROLE_CATEGORY_MAP.get(role, role)

    if "Job Category" not in df.columns:
        return {"error": "'Job Category' column not found in data."}

    role_df = df[df["Job Category"] == category]

    if len(role_df) < 3:
        return {"error": f"Not enough data for role: {role}"}

    available_skills = [s for s in SKILLS if s in df.columns]
    role_skill_counts = role_df[available_skills].sum().sort_values(ascending=False)

    top_skills = role_skill_counts.head(10).index.tolist()
    missing_skills = [s for s in top_skills if s not in user_skills]

    return {
        "Role": role,
        "Required Skills": top_skills,
        "Your Skills": user_skills,
        "Skills To Learn": missing_skills
    }

ROLE_SUGGESTED_SKILLS = {
    "Data Analyst": ["Python", "Sql", "Excel", "Tableau", "Power bi", "Statistics", "R"],
    "Data Scientist": ["Python", "R", "Machine learning", "Deep learning", "Tensorflow", "Pytorch", "Statistics", "Pandas", "Numpy", "Scikit-learn"],
    "Data Engineer": ["Python", "Sql", "Spark", "Kafka", "Airflow", "Aws", "Gcp", "Azure", "Hadoop", "Databricks", "Dbt"],
    "Business Analyst": ["Excel", "Sql", "Tableau", "Power bi", "Communication", "Presentation", "Project management", "Jira"],
    "Senior Analyst": ["Python", "Sql", "Tableau", "Power bi", "Leadership", "Project management"],
    "Junior Analyst": ["Excel", "Sql", "Python", "Tableau", "Communication"],
    "Technical Analyst": ["Sql", "Python", "Git", "Docker", "Nosql", "Postgresql"]
}
