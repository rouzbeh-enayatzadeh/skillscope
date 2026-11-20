import hashlib
import re


def normalize_text(text: str) -> str:
    """Lowercase and collapse all whitespace to single spaces."""
    return re.sub(r"\s+", " ", str(text).lower()).strip()


def text_hash(text: str) -> str:
    """Short fingerprint of a normalized text: same text → same hash."""
    return hashlib.md5(normalize_text(text).encode("utf-8")).hexdigest()[:12]
