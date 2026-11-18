# skillscope
What data &amp; AI jobs really ask for, and what they pay: skill extraction, salary prediction and CV matching on job postings.

## Data

Main dataset: [LinkedIn Job Postings (2023-2024)](https://www.kaggle.com/datasets/arshkon/linkedin-job-postings) by arshkon, license CC BY-SA 4.0.

Setup (needs a Kaggle API token in `~/.kaggle/access_token`):

    uv venv && source .venv/bin/activate
    uv pip install -r requirements.txt
    kaggle datasets download -d arshkon/linkedin-job-postings -p data/raw/linkedin --unzip

The `data/` folder is gitignored and never committed.