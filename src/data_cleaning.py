import pandas as pd
from src.config import RAW_DATA_PATH, CLEANED_DATA_PATH, PROCESSED_DIR

def clean_data(input_path, output_path):

    df = pd.read_csv(input_path)

    df = df.drop(["Unnamed: 0", "Competitors", "Easy Apply"], axis=1, errors="ignore")

    df = df.dropna(subset=["Company Name"])
    df["Industry"] = df["Industry"].fillna("Unknown")
    df["Sector"] = df["Sector"].fillna("Unknown")
    
    def categorize_job_title(title):
        if pd.isna(title):
            return "Other"
        title = title.lower()
        if any(word in title for word in ["senior", "sr", "lead", "principal", "manager", "iii"]):
            return "Senior Analyst"
        elif any(word in title for word in ["junior", "jr", "entry", "intern", "i"]):
            return "Junior Analyst"
        elif any(word in title for word in ["business", "financial", "marketing", "sales"]):
            return "Business Analyst"
        elif any(word in title for word in ["technical", "sql", "systems", "database", "quality", "governance", "warehouse"]):
            return "Technical Analyst"
        elif "data scientist" in title or "machine learning" in title:
            return "Data Scientist"
        elif "data engineer" in title:
            return "Data Engineer"
        else:
            return "Data Analyst (General)"

    df["Job Category"] = df["Job Title"].apply(categorize_job_title)

    if "Salary Estimate" in df.columns:
        df["Salary Estimate Clean"] = df["Salary Estimate"].astype(str)\
            .str.replace(r"\(.*\)", "", regex=True)\
            .str.replace("K", "", regex=False)\
            .str.replace("$", "", regex=False)\
            .str.strip()
            
        salary_split = df["Salary Estimate Clean"].str.split("-", expand=True)
        df["salary_min"] = pd.to_numeric(salary_split[0], errors="coerce")
        df["salary_max"] = pd.to_numeric(salary_split[1], errors="coerce")
        df["salary_avg"] = (df["salary_min"] + df["salary_max"]) / 2

    df = df.drop_duplicates().reset_index(drop=True)
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

if __name__ == "__main__":
    clean_data(RAW_DATA_PATH, CLEANED_DATA_PATH)
