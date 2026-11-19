# SkillScope

What data & AI jobs really ask for, and what they pay: skill extraction, salary prediction and CV matching on job postings.

## Data

- Main dataset: [LinkedIn Job Postings (2023-2024)](https://www.kaggle.com/datasets/arshkon/linkedin-job-postings) by arshkon, license CC BY-SA 4.0.
- Second dataset: [Data Analyst Job Postings (Google search)](https://www.kaggle.com/datasets/lukebarousse/data-analyst-job-postings-google-search) by Luke Barousse, license Apache 2.0. Collection stopped in April 2025.

## Setup

Needs a Kaggle API token in `~/.kaggle/access_token`.

    uv venv && source .venv/bin/activate
    uv pip install -r requirements.txt
    kaggle datasets download -d arshkon/linkedin-job-postings -p data/raw/linkedin --unzip
    kaggle datasets download -d lukebarousse/data-analyst-job-postings-google-search -p data/raw/gsearch --unzip

The `data/` folder is gitignored and never committed.