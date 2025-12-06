import pdfplumber
import re
from typing import List

def extract_text_from_pdf(path: str) -> str:
    texts = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            texts.append(page.extract_text() or "")
    return "\n".join(texts)

def chunk_text(text: str, max_words: int = 250) -> List[str]:
    words = re.split(r"(\s+)", text)
    chunks = []
    cur = []
    cur_words = 0
    for token in words:
        if token.strip() == "":
            cur.append(token)
            continue
        cur.append(token)
        cur_words += 1
        if cur_words >= max_words:
            chunks.append("".join(cur).strip())
            cur = []
            cur_words = 0
    if cur:
        chunks.append("".join(cur).strip())
    return [c for c in chunks if c]
