# ingestion.py
"""
Cleans and chunks the raw Wikipedia JSON from data/raw/ into retrieval-ready
chunks to data/processed/
"""

# Import libraries
from pathlib import Path
import json
import re
import unicodedata

# Constants
RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
PROCESSED_DIR = Path(__file__).parent.parent / "data" / "processed"
OUTPUT_FILE = PROCESSED_DIR / "chunks.json"
CHUNK_SIZE = 700  # characters per chunk
CHUNK_OVERLAP = 80  # character overlap between chunks
MIN_SECTION_SIZE = 150  # header/body sections shorter will get folded into the next section
MIN_CHUNK_SIZE = 200  # chunks shorter than this will get folded into the previous chunk

# Matches headers, e.g., "== Name ==", "=== Etymology ==="
HEADER_PATTERN = re.compile(r"^(={2,4})\s*(.+?)\s*\1\s*$", re.MULTILINE)

# Translate Old Norse/Icelandic letters for texts like "Þóra borgarhjǫrtr" and "Ælla"
NORSE_CHAR_MAP = str.maketrans({"Þ": "Th", 
                                "þ": "th",
                                "Ð": "D", 
                                "ð": "d",
                                "Æ": "Ae", 
                                "æ": "ae",
                                "Ø": "O", 
                                "ø": "o",
                                "ǫ": "o", 
                                "Ǫ": "O"})


def clean_text(text: str) -> str:
    """Cleans text"""

    # Remove citation markers like [1], [23]
    text = re.sub(r"\[\d+\]", "", text)

    # Remove stray [edit]-style links
    text = re.sub(r"\[edit\]", "", text, flags = re.IGNORECASE)

    # Collapse 3+ newlines down to a double newline (paragraph break)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Collapse repeated spaces and tabs
    text = re.sub(r"[ \t]{2,}", " ", text)

    # Trim trailing whitespace on each line
    text = "\n".join(line.rstrip() for line in text.split("\n"))

    return text.strip()


def split_into_sections(text: str) -> list[dict]:
    """Splits article text into headers with their bodies"""

    # Find headers
    matches = list(HEADER_PATTERN.finditer(text))

    sections = []

    # Anything before the first header gets placed in the Introduction header
    lead_end = matches[0].start() if matches else len(text)
    lead_body = clean_text(text[:lead_end])
    if lead_body:
        sections.append({"heading": "Introduction", "body": lead_body})

    # For each header, extract its body text
    for i, match in enumerate(matches):
        heading = match.group(2).strip()
        body_start = match.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = clean_text(text[body_start:body_end])

        if not body:
            continue

        sections.append({"heading": heading, "body": body})

    return sections


def merge_short_sections(sections: list[dict]) -> list[dict]:
    """
    Adds sections shorter than MIN_SECTION_SIZE into the next section.
    A trailing short section is added to the section before it
    """

    if not sections:
        return sections

    merged = []
    carry_over = ""

    # Fold short sections into the next section
    for section in sections:
        heading = section["heading"]
        body = (carry_over + " " + section["body"]).strip() if carry_over else section["body"]
        carry_over = ""

        # if body of header is too short, carry it forward into the next section
        if len(body) < MIN_SECTION_SIZE:
            carry_over = f"{heading}: {body}"
            continue

        merged.append({"heading": heading, "body": body})

    # If the last section is short, fold it into the previous section
    if carry_over and merged:
        merged[-1]["body"] = (merged[-1]["body"] + " " + carry_over).strip()
    # If entire article has no section long enough to stand alone, add it to Introduction header
    elif carry_over:
        merged.append({"heading": "Introduction", "body": carry_over})

    return merged


def sliding_window_split(text: str, chunk_size: int, overlap: int) -> list[str]:
    """
    Splits text into overlapping chunks on paragraph/sentence-friendly
    boundaries where possible
    """

    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size

        if end < len(text):
            min_boundary = start + (chunk_size // 2)
            boundary = text.rfind("\n\n", min_boundary, end)
            if boundary == -1:
                boundary = text.rfind(". ", min_boundary, end)
            if boundary != -1:
                end = boundary + 1

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = max(end - overlap, start + 1)

        # Prevent overlap from starting mid-word by starting on the next word
        if start < len(text) and not text[start - 1].isspace():
            next_space = text.find(" ", start)
            if next_space != -1 and next_space < end:
                start = next_space + 1

    # If the last chunk is short, fold it into the previous chunk
    if len(chunks) > 1 and len(chunks[-1]) < MIN_CHUNK_SIZE:
        last = chunks.pop()
        chunks[-1] = (chunks[-1] + " " + last).strip()

    return chunks


def build_chunks_for_article(article: dict) -> list[dict]:
    """Turns an article into a list of chunk dicts for embedding"""

    sections = split_into_sections(article["text"])
    # sections = merge_short_sections(sections) # add if short-section chunks are noisy

    chunks = []
    for section in sections:
        pieces = sliding_window_split(section["body"], CHUNK_SIZE, CHUNK_OVERLAP)
        for i, piece in enumerate(pieces):
            chunks.append({"text": piece,
                           "metadata": {"title": article["title"],
                                        "category": article["category"],
                                        "section_heading": section["heading"],
                                        "source_url": article["url"],
                                        "license": article["license"]}         
                                        })

    return chunks


def load_raw_articles() -> list[dict]:
    """Loads all fetched articles in data/raw/"""

    articles = []
    for path in sorted(RAW_DIR.glob("*.json")):
        with open(path, encoding = "utf-8") as f:
            articles.append(json.load(f))
    return articles


def build_all_chunks() -> list[dict]:
    """
    Runs the full ingestion pipeline. Loads all articles and creates
    chunks for every one. Returns a list of chunk dicts, with each 
    chunk having an id
    """

    # Load all articles and create chunks for each one
    all_chunks = []
    for article in load_raw_articles():
        all_chunks.extend(build_chunks_for_article(article))

    # Assign ids to each chunk
    for i, chunk in enumerate(all_chunks):
        title = chunk["metadata"]["title"].translate(NORSE_CHAR_MAP)
        ascii_title = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode()
        slug = re.sub(r"[^a-z0-9]+", "_", ascii_title.lower()).strip("_")
        chunk["chunk_id"] = f"{slug}_{i:04d}"

    return all_chunks


def save_chunks(chunks: list[dict], output_file: Path = OUTPUT_FILE) -> None:
    """Saves chunks to data/processed/"""

    output_file.parent.mkdir(parents = True, exist_ok = True)
    with open(output_file, "w", encoding = "utf-8") as f:
        json.dump(chunks, f, indent = 2, ensure_ascii = False)


def main() -> list[dict]:
    """Builds chunks from articles in data/raw/ and saves them to data/processed/"""

    chunks = build_all_chunks()
    save_chunks(chunks)
    print(f"Wrote {len(chunks)} chunks from {len(list(RAW_DIR.glob('*.json')))} "
          f"articles to {OUTPUT_FILE}")
    return chunks


if __name__ == "__main__":
    main()
