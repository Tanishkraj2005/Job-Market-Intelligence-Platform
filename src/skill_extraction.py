import pandas as pd
from src.config import SKILLS, CLEANED_DATA_PATH, SKILL_MATRIX_PATH

import re

def extract_skills(input_path, output_path):

    df = pd.read_csv(input_path)

    df["Job Description"] = df["Job Description"].fillna("").str.lower()

    for skill in SKILLS:
        pattern = r'(?<!\w)' + re.escape(skill) + r'(?!\w)'
        df[skill] = df["Job Description"].str.contains(pattern, regex=True, na=False).astype(int)
        
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

if __name__ == "__main__":
    extract_skills(CLEANED_DATA_PATH, SKILL_MATRIX_PATH)
