import streamlit as st
import pandas as pd
import plotly.express as px
from src.config import SKILLS, SKILL_MATRIX_PATH, CLEANED_DATA_PATH
from src.salary_gap_analyzer import calculate_salary_gap
from src.role_fit_analyzer import calculate_role_fit
from src.career_recommendation import career_skill_gap, ROLE_SUGGESTED_SKILLS, ROLE_CATEGORY_MAP
from src.salary_analysis import salary_by_skill, salary_by_skill_for_role
from src.network_analysis import build_network, build_network_for_role
from src.recommendation_engine import recommend_skills

st.set_page_config(page_title="DataAnalytics Career Hub", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .recommendation-card {
        background: #1e2130; padding: 16px 20px; border-radius: 10px;
        margin-bottom: 12px; border-left: 5px solid #00d2ff; transition: transform 0.2s;
    }
    .recommendation-card:hover { transform: translateX(4px); }
    .role-card {
        background: #1e2130; padding: 18px 20px; border-radius: 10px;
        margin-bottom: 12px; border-top: 4px solid #ff4b4b; transition: transform 0.2s;
    }
    .role-card:hover { transform: translateY(-2px); }
    .skill-tag {
        display: inline-block; background: #00d2ff22; color: #00d2ff;
        border: 1px solid #00d2ff55; padding: 4px 12px; border-radius: 20px;
        font-size: 0.85em; font-weight: 600; margin: 3px;
    }
    .missing-tag {
        display: inline-block; background: #ff4b4b22; color: #ff4b4b;
        border: 1px solid #ff4b4b55; padding: 4px 12px; border-radius: 20px;
        font-size: 0.85em; font-weight: 600; margin: 3px;
    }
</style>
                                    <div class="recommendation-card">
                                        <b style="color:#00d2ff;">{rec['skill'].capitalize()}</b>
                                        <span style="color:#4CAF50; margin-left:8px;">(+${rec['boost']:.1f}K)</span>
                                        <p style="margin:6px 0 0; color:#ccc;">Raises avg salary to <strong>${rec['new_salary']:.1f}K</strong></p>
                                    </div>
                                    <div class="role-card">
                                        <div style="display:flex; justify-content:space-between; align-items:center;">
                                            <b style="font-size:1.1em;">{fit['role']}</b>
                                            <span style="color:{color}; font-weight:700; font-size:1.1em;">{fit['fit_score']}%</span>
                                        </div>
                                        <p style="margin:8px 0 4px; color:#aaa; font-size:0.85em;">Key skills for this role:</p>
                                        <div>{''.join([f'<span class="skill-tag">{s.capitalize()}</span>' for s in fit["key_skills"]])}</div>
                                    </div>
                                    """, unsafe_allow_html=True)
                        else:
                            st.warning("No matching roles found.")
                    except Exception as e:
                        st.error(str(e))
