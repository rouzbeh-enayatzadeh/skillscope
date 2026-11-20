import re

from tokenizers import Tokenizer

# Split on line breaks, bullet characters, and sentence ends (also "end.Next" without a space).
_UNIT_SPLIT = re.compile(r"\n+|\s*[•●▪]\s*|(?<=[.!?])\s*(?=[A-Z])")


def load_tokenizer(name: str = "sentence-transformers/all-MiniLM-L6-v2") -> Tokenizer:
    """Tokenizer of the embedding model, without truncation or padding."""
    tok = Tokenizer.from_pretrained(name)
    tok.no_truncation()
    tok.no_padding()
    return tok


def n_tokens(text: str, tokenizer: Tokenizer) -> int:
    """Number of tokens without the special [CLS] / [SEP] tokens."""
    return len(tokenizer.encode(text, add_special_tokens=False).ids)


def split_units(text: str) -> list:
    """Split a description into small units: lines, bullet points, sentences."""
    units = (u.strip() for u in _UNIT_SPLIT.split(str(text)))
    return [u for u in units if u]


def split_long_unit(unit: str, tokenizer: Tokenizer, window: int) -> list:
    """Cut a too-long unit into word windows of at most `window` tokens (never inside a word)."""
    pieces, current, current_len = [], [], 0
    for word in unit.split():
        n = n_tokens(word, tokenizer)
        if current and current_len + n > window:
            pieces.append(" ".join(current))
            current, current_len = [], 0
        current.append(word)
        current_len += n
    if current:
        pieces.append(" ".join(current))
    return pieces


def chunk_text(text: str, tokenizer: Tokenizer, max_tokens: int = 200, min_tokens: int = 20) -> list:
    """Pack consecutive units into chunks of at most max_tokens tokens.

    Units longer than max_tokens are first cut into word windows of max_tokens // 2,
    so a short heading before them can still share a chunk. A last chunk shorter than
    min_tokens is merged into the previous one (still below the model's 256 limit).
    """
    units = []
    for unit in split_units(text):
        if n_tokens(unit, tokenizer) > max_tokens:
            units.extend(split_long_unit(unit, tokenizer, max_tokens // 2))
        else:
            units.append(unit)

    chunks, current, current_len = [], [], 0
    for unit in units:
        n = n_tokens(unit, tokenizer)
        if current and current_len + n > max_tokens:
            chunks.append(" ".join(current))
            current, current_len = [], 0
        current.append(unit)
        current_len += n
    if current:
        chunks.append(" ".join(current))

    # A very small last chunk carries little meaning on its own: merge it into the previous one.
    if len(chunks) > 1 and n_tokens(chunks[-1], tokenizer) < min_tokens:
        tail = chunks.pop()
        chunks[-1] = chunks[-1] + " " + tail
    return chunks