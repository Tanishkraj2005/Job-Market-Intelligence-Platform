# DataAnalytics Career Hub

A Streamlit web application that analyzes an actual Glassdoor job postings dataset to give data professionals a clear, data-driven view of the job market. It calculates skill gaps, estimates salaries based on your skills, and uses co-occurrence networks to recommend which skill you should learn next.

## Setup Instructions

1. Clone this repository
2. Create and activate a virtual environment (`python -m venv venv`)
3. Install the required libraries:
   `pip install -r requirements.txt`
4. Run the data pipeline to prepare the dataset:
   `python run_pipeline.py`
5. Start the web app:
   `streamlit run app.py`

## Features

- **Skill Network & Demand**: Explores the most in-demand skills for different data roles based on network centrality.
- **Salary by Skill**: Analyzes average salaries attached to specific skills in job postings.
- **Next Skill Recommender**: Recommends the next most logical skill to learn based on what you already know.
- **Role Skill Gap**: Compare your current skills against top requirements for your target role.
- **Salary Gap Analyzer**: See what skills can bridge the gap between your current market value and target salary.
- **Role Fit Quiz**: Scores your resume skills across all job categories.

## Project Structure

- `app.py`: The Streamlit dashboard
- `run_pipeline.py`: Executes the data cleaning and extraction process
- `src/`: Python modules containing core logic for cleaning, network analysis, and recommendations
- `notebooks/`: Jupyter notebooks used for initial EDA and modeling exploration
- `Data/`: Directory where the raw Glassdoor dataset and processed results are stored

## Data

The original raw data comes from a scraped dataset of over 6,500 Glassdoor Data Analyst and related job postings. The pipeline processes this to build a binary skill matrix across 88 mapped skills and calculates average salary ranges.

## License

MIT
