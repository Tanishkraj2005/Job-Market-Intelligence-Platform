import os
import sys
import yaml
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "Data"
RAW_DATA_PATH = DATA_DIR / "Raw" / "DataAnalyst.csv"
PROCESSED_DIR = DATA_DIR / "processed"
CLEANED_DATA_PATH = PROCESSED_DIR / "cleaned_jobs.csv"
SKILL_MATRIX_PATH = PROCESSED_DIR / "skill_matrix.csv"

_SKILLS_FILE = Path(__file__).resolve().parent / "skills.yaml"
with open(_SKILLS_FILE, "r", encoding="utf-8") as f:
    SKILLS = yaml.safe_load(f)["skills"]
