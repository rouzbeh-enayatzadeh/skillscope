import re

# canonical name: (category, [regex patterns])
# All patterns are matched case-insensitively, except parts wrapped in (?-i:...).
SKILLS = {
    # Programming languages
    "python":        ("language", [r"\bpython\b"]),
    "r":             ("language", [r"(?-i:\bR\b)(?![&\-'.])"]),
    "sql":           ("language", [r"\bsql\b"]),
    "scala":         ("language", [r"\bscala\b"]),
    "java":          ("language", [r"\bjava\b"]),
    "javascript":    ("language", [r"\bjavascript\b", r"(?-i:\bJS\b)"]),
    "typescript":    ("language", [r"\btypescript\b"]),
    "c++":           ("language", [r"(?<!\w)c\+\+"]),
    "c#":            ("language", [r"(?<!\w)c#", r"\bc sharp\b"]),
    "c":             ("language", [r"(?-i:(?<![\w&])C)(?=\s*(?:,|/|\bor\b|\band\b))"]),
    "go":            ("language", [r"\bgolang\b", r"(?-i:\bGo\b)(?=\s*(?:,|/|\)|\bor\b|\band\b))"]),
    "rust":          ("language", [r"(?-i:\bRust\b)"]),
    "bash":          ("language", [r"\bbash\b", r"\bshell script(?:s|ing)?\b"]),
    "vba":           ("language", [r"\bvba\b"]),
    "sas":           ("language", [r"(?-i:\bSAS\b)"]),
    "matlab":        ("language", [r"\bmatlab\b"]),
    # Databases and warehouses
    "postgresql":    ("database", [r"\bpostgres(?:ql)?\b"]),
    "mysql":         ("database", [r"\bmysql\b"]),
    "sql server":    ("database", [r"\bsql server\b", r"\bmssql\b", r"\bt-?sql\b"]),
    "oracle":        ("database", [r"\boracle\b"]),
    "mongodb":       ("database", [r"\bmongo(?:db)?\b"]),
    "nosql":         ("database", [r"\bno-?sql\b"]),
    "redis":         ("database", [r"\bredis\b"]),
    "snowflake":     ("database", [r"\bsnowflake\b"]),
    "bigquery":      ("database", [r"\bbig ?query\b"]),
    "redshift":      ("database", [r"\bredshift\b"]),
    "databricks":    ("database", [r"\bdatabricks\b"]),
    "elasticsearch": ("database", [r"\belastic ?search\b"]),
    # Cloud and infrastructure
    "aws":           ("cloud", [r"\baws\b", r"\bamazon web services\b"]),
    "azure":         ("cloud", [r"\bazure\b"]),
    "gcp":           ("cloud", [r"\bgcp\b", r"\bgoogle cloud\b"]),
    "docker":        ("cloud", [r"\bdocker\b"]),
    "kubernetes":    ("cloud", [r"\bkubernetes\b", r"\bk8s\b"]),
    "terraform":     ("cloud", [r"\bterraform\b"]),
    "git":           ("cloud", [r"\bgit\b", r"\bgithub\b", r"\bgitlab\b", r"\bbitbucket\b"]),
    "linux":         ("cloud", [r"\blinux\b", r"\bunix\b"]),
    "ci/cd":         ("cloud", [r"\bci ?/ ?cd\b", r"\bcontinuous integration\b"]),
    # Data engineering
    "spark":         ("data_engineering", [r"\bpyspark\b", r"\bapache spark\b", r"(?-i:\bSpark\b)"]),
    "hadoop":        ("data_engineering", [r"\bhadoop\b"]),
    "kafka":         ("data_engineering", [r"\bkafka\b"]),
    "airflow":       ("data_engineering", [r"\bairflow\b"]),
    "dbt":           ("data_engineering", [r"\bdbt\b"]),
    "etl":           ("data_engineering", [r"\betl\b", r"\belt\b"]),
    "ssis":          ("data_engineering", [r"\bssis\b"]),
    "informatica":   ("data_engineering", [r"\binformatica\b"]),
    "data modeling": ("data_engineering", [r"\bdata model(?:l)?ing\b"]),
    # BI and analytics
    "excel":         ("bi", [r"(?-i:\bExcel\b)", r"\b(?:ms|microsoft) excel\b"]),
    "power bi":      ("bi", [r"\bpower ?bi\b"]),
    "tableau":       ("bi", [r"\btableau\b"]),
    "looker":        ("bi", [r"\blooker\b"]),
    "qlik":          ("bi", [r"\bqlik(?:view| ?sense)?\b"]),
    "ssrs":          ("bi", [r"\bssrs\b"]),
    "dax":           ("bi", [r"\bdax\b"]),
    "powerpoint":    ("bi", [r"\bpower ?points?\b"]),
    "alteryx":       ("bi", [r"\balteryx\b"]),
    "data visualization": ("bi", [r"\bdata visuali[sz]ation\b"]),
    # Concepts
    "statistics":    ("concept", [r"\bstatistic(?:s|al)\b"]),
    "a/b testing":   ("concept", [r"\ba/?b test(?:s|ing)?\b", r"\bexperiment(?:ation)? design\b"]),
    "time series":   ("concept", [r"\btime[- ]series\b"]),
    # Machine learning
    "machine learning": ("ml", [r"\bmachine learning\b", r"(?-i:\bML\b)"]),
    "deep learning": ("ml", [r"\bdeep learning\b", r"\bneural networks?\b"]),
    "nlp":           ("ml", [r"\bnlp\b", r"\bnatural language processing\b"]),
    "computer vision": ("ml", [r"\bcomputer vision\b", r"\bopencv\b"]),
    "scikit-learn":  ("ml", [r"\bscikit[- ]?learn\b", r"\bsklearn\b"]),
    "pandas":        ("ml", [r"\bpandas\b"]),
    "numpy":         ("ml", [r"\bnumpy\b"]),
    "scipy":         ("ml", [r"\bscipy\b"]),
    "tensorflow":    ("ml", [r"\btensorflow\b"]),
    "pytorch":       ("ml", [r"\bpytorch\b"]),
    "keras":         ("ml", [r"\bkeras\b"]),
    "xgboost":       ("ml", [r"\bxgboost\b"]),
    "lightgbm":      ("ml", [r"\blightgbm\b"]),
    "mlflow":        ("ml", [r"\bmlflow\b"]),
    "mlops":         ("ml", [r"\bmlops\b"]),
    "jupyter":       ("ml", [r"\bjupyter\b"]),
    # Generative AI
    "llm":           ("genai", [r"\bllms?\b", r"\blarge language models?\b"]),
    "generative ai": ("genai", [r"\bgenerative ai\b", r"\bgen ?ai\b"]),
    "rag":           ("genai", [r"(?-i:\bRAG\b)", r"\bretrieval[- ]augmented\b"]),
    "langchain":     ("genai", [r"\blangchain\b"]),
    "llamaindex":    ("genai", [r"\bllama ?index\b"]),
    "hugging face":  ("genai", [r"\bhugging ?face\b"]),
    "openai":        ("genai", [r"\bopenai\b"]),
    "prompt engineering": ("genai", [r"\bprompt engineering\b"]),
    "vector database": ("genai", [r"\bvector (?:database|db|store)s?\b", r"\bpinecone\b",
                                  r"\bfaiss\b", r"\bweaviate\b"]),
    # Web and APIs
    "fastapi":       ("web", [r"\bfastapi\b"]),
    "flask":         ("web", [r"\bflask\b"]),
    "streamlit":     ("web", [r"\bstreamlit\b"]),
    "rest api":      ("web", [r"\brest(?:ful)? apis?\b"]),
}

SKILL_CATEGORY = {name: cat for name, (cat, _) in SKILLS.items()}

# Compile once at import time: one regex per skill (all its patterns joined with |).
_COMPILED = {
    name: re.compile("|".join(f"(?:{p})" for p in patterns), re.IGNORECASE)
    for name, (_, patterns) in SKILLS.items()
}


def extract_skills(text: str) -> set:
    """Return the set of canonical skill names found in a text."""
    if not isinstance(text, str):
        return set()
    return {name for name, rx in _COMPILED.items() if rx.search(text)}
