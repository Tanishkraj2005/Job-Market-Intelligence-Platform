# DataAnalytics Career Hub

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Interactive-FF4B4B?logo=streamlit)
![Power BI](https://img.shields.io/badge/Power_BI-Dashboard-F2C811?logo=powerbi)
![NetworkX](https://img.shields.io/badge/NetworkX-Graph_Analysis-lightgrey)

A full-stack data analytics and career intelligence platform designed to help data professionals (Data Analysts, Scientists, Engineers) make data-driven career choices. Rather than relying on generic advice, the system analyzes raw job market data to provide personalized recommendations.

### 🚀 Live Demos
* **Web Application:** [View the Interactive Streamlit App](https://job-market-intelligence-platform.streamlit.app/)
* **Executive Dashboard:** [View the Power BI Dashboard](https://app.powerbi.com/groups/me/reports/33caa299-827e-4e3d-a2cc-ffc6d7fc1e34/20e85ea10102aa407a28?experience=power-bi)

---

## 🏗️ Project Architecture

The application architecture is split into three main components:

1. **Data Engineering Pipeline**
   An ETL script (`run_pipeline.py`) that cleans the raw Glassdoor postings, standardizes job categories, extracts salary ranges, and builds an 88-column binary skill matrix using RegEx text mining.

2. **Analytics Engine**
   Core Python modules (`src/`) that handle graph network centrality, skill co-occurrence scoring, and probabilistic role-fit math.

3. **Interactive Frontend & BI Layers**
   A Streamlit dashboard (`app.py`) that filters insights based on the user's current skills, supported by a macro-level Power BI Executive Dashboard.

---

## 🎯 Core Features

* **Skill Network & Demand:** Calculates NetworkX degree centrality to find the most interconnected and highly demanded skills for specific roles.
* **Salary by Skill:** Aggregates and ranks the exact average salaries commanded by specific technical skills in the actual job market.
* **Next Skill Recommender:** A co-occurrence recommendation engine that suggests the most logical next skill to learn based on your existing stack.
* **Job Role Skill Gap:** Visualizes exactly what skills you are missing for top roles in the industry.
* **Salary Gap Analyzer:** Calculates your current estimated market value and shows exactly which skill addition provides the highest salary boost.
* **Role Fit Quiz:** Scores your resume objectively against all major data job categories.

---

## 💻 Setup and Installation

### Prerequisites
* Python 3.10+
* Minimum 4GB RAM (for data processing)

### Local Environment Setup

1. Clone the repository:
```bash
git clone https://github.com/Tanishkraj2005/Job-Market-Intelligence-Platform.git
cd Job-Market-Intelligence-Platform
```

2. Create and activate a virtual environment:
```bash
python -m venv venv

# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the data pipeline (this generates the processed datasets):
```bash
python run_pipeline.py
```

5. Launch the Streamlit dashboard:
```bash
streamlit run app.py
```

---

## 📊 The Dataset
The raw data (`Data/Raw/DataAnalyst.csv`) is a scraped dataset of over 6,500 Glassdoor job postings. The pipeline processes this into `cleaned_jobs.csv` and `skill_matrix.csv`, which are used heavily for visualizations and modeling. 

Skill mapping is controlled via `src/skills.yaml`, allowing for zero-code additions of new tracked technologies.

## 📄 License
This project is open-source and licensed under the MIT License.
