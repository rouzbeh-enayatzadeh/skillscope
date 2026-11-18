import re

ROLE_PATTERNS = [
    ("ML/AI Engineer", r"machine learning|\bml\b|\bai\b|deep learning|\bnlp\b|computer vision|\bllm\b|mlops"),
    ("Data Scientist", r"scien"),
    ("Data Engineer", r"engineer|architect|\betl\b|warehouse"),
    ("BI Analyst", r"business intelligence|\bbi\b|power bi|tableau"),
    ("Data Analyst", r"analy"),
]


def role_family(title: str) -> str:
    """Map a job title to a role family. First matching pattern wins."""
    t = str(title).lower()
    for role, pattern in ROLE_PATTERNS:
        if re.search(pattern, t):
            return role
    return "Other"