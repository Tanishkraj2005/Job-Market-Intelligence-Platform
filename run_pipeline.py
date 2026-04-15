import os
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.config import RAW_DATA_PATH, CLEANED_DATA_PATH, SKILL_MATRIX_PATH
from src.data_cleaning import clean_data
from src.skill_extraction import extract_skills
from src.network_analysis import build_network
from src.salary_analysis import salary_by_skill
from src.recommendation_engine import recommend_skills

def main():

    logging.info("Step 1: Cleaning data...")
    clean_data(RAW_DATA_PATH, CLEANED_DATA_PATH)

    logging.info("Step 2: Extracting skills...")
    extract_skills(CLEANED_DATA_PATH, SKILL_MATRIX_PATH)

    logging.info("Step 3: Building skill network...")
    G, centrality = build_network(SKILL_MATRIX_PATH)
    logging.info("Top central skills:")
    logging.info(str(sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:5]))

    logging.info("Step 4: Salary analysis...")
    salary_df = salary_by_skill(SKILL_MATRIX_PATH)
    logging.info("\n" + str(salary_df.sort_values(by="Average Salary", ascending=False).head()))

    logging.info("Step 5: Skill recommendation example...")
    rec = recommend_skills(SKILL_MATRIX_PATH, ["excel", "sql"])
    logging.info(str(rec))

    logging.info("Pipeline completed successfully.")

if __name__ == "__main__":
    main()
