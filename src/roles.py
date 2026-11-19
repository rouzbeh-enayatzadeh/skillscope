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

SENIORITY_PATTERNS = [
    ("Intern", r"\bintern"),
    ("Lead/Principal", r"\blead\b|\bprincipal\b|\bstaff\b|\bhead of\b|\bdirector\b|\bmanager\b"),
    ("Senior", r"\bsenior\b|\bsr\b|\biii\b|\biv\b"),
    ("Junior", r"\bjunior\b|\bjr\b|\bentry\b"),
]


def seniority_from_title(title: str) -> str:
    """Map a job title to a seniority level. First matching pattern wins."""
    t = str(title).lower()
    for level, pattern in SENIORITY_PATTERNS:
        if re.search(pattern, t):
            return level
    return "Not stated"

def combine_seniority(title_level: str, linkedin_level) -> str:
    """Title keywords first, LinkedIn's experience level as fallback."""
    li = linkedin_level if isinstance(linkedin_level, str) else ""

    if title_level == "Intern" or li == "Internship":
        return "Intern"
    if li in ("Director", "Executive"):
        return "Director+"
    if title_level in ("Lead/Principal", "Senior", "Junior"):
        return title_level
    if li in ("Entry level", "Associate"):
        return "Junior"
    if li == "Mid-Senior level":
        return "Mid-Senior"
    return "Unknown"

