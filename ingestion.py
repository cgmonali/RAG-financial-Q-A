from pathlib import Path
from bs4 import BeautifulSoup
from typing import Dict

def load_html_texts(folder: str) -> Dict[str, str]:
    texts = {}
    for file in Path(folder).glob("*.html"):
        with open(file, "r", encoding="utf-8", errors="ignore") as f:
            soup = BeautifulSoup(f, "html.parser")
            text = soup.get_text(separator=" ", strip=True)
            texts[file.stem] = text
    return texts
