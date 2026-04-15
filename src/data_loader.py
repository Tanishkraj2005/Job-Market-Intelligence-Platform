import streamlit as st
import pandas as pd
from src.config import SKILL_MATRIX_PATH, CLEANED_DATA_PATH

@st.cache_data
def load_csv(data_path):
    return pd.read_csv(data_path)
