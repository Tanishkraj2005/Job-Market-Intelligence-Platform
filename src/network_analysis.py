import pandas as pd
import networkx as nx
from src.config import SKILLS, SKILL_MATRIX_PATH
from src.data_loader import load_csv

def build_network(data_path=SKILL_MATRIX_PATH):

    df = load_csv(data_path)

    available_skills = [s for s in SKILLS if s in df.columns]
    skill_matrix = df[available_skills]

    co_occurrence = skill_matrix.T.dot(skill_matrix)

    G = nx.from_pandas_adjacency(co_occurrence)

    centrality = nx.degree_centrality(G)

    return G, centrality

def build_network_for_role(job_category, data_path=SKILL_MATRIX_PATH):
    df = load_csv(data_path)

    if "Job Category" in df.columns and job_category:
        df = df[df["Job Category"] == job_category]

    if df.empty:
        return None, {}

    available_skills = [s for s in SKILLS if s in df.columns]
    skill_matrix = df[available_skills]

    co_occurrence = skill_matrix.T.dot(skill_matrix)

    G = nx.from_pandas_adjacency(co_occurrence)
    centrality = nx.degree_centrality(G)

    return G, centrality
