# fetch_sources.py
"""
Pulls content from Wikipedia and saves them to data/raw/
"""

# Import libraries
from pathlib import Path
import requests
import json
from datetime import date
import time
import re

# Constants
RAW_DIR = Path(__file__).parent / "raw"
WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"
USER_AGENT = "NorseMythologyProject"
LICENSE_NOTE = "CC BY-SA 4.0 (Wikipedia text) - https://creativecommons.org/licenses/by-sa/4.0/"
ARTICLES = [
    # saga/history
    {"title": "Ragnar Lodbrok", "filename": "ragnar_lodbrok.md", "category": "saga_history"},
    {"title": "Tale of Ragnar Lodbrok", "filename": "tale_of_ragnar_lodbrok.md", "category": "saga_history"},
    {"title": "Lagertha", "filename": "lagertha.md", "category": "saga_history"},
    {"title": "Þóra borgarhjǫrtr", "filename": "thora_borgarhjortr.md", "category": "saga_history"},
    {"title": "Aslaug", "filename": "aslaug.md", "category": "saga_history"},
    {"title": "Björn Ironside", "filename": "bjorn_ironside.md", "category": "saga_history"},
    {"title": "Ivar the Boneless", "filename": "ivar_the_boneless.md", "category": "saga_history"},
    {"title": "Sigurd Snake-in-the-Eye", "filename": "sigurd_snake_in_the_eye.md", "category": "saga_history"},
    {"title": "Siege of Paris (845)", "filename": "siege_of_paris_845.md", "category": "saga_history"},
    {"title": "Early Scandinavian Dublin", "filename": "early_scandinavian_dublin.md", "category": "saga_history"},
    {"title": "Ælla of Northumbria", "filename": "aella_of_northumbria.md", "category": "saga_history"},
    {"title": "Great Heathen Army", "filename": "great_heathen_army.md", "category": "saga_history"},
    # mythology
    {"title": "Old Norse religion", "filename": "old_norse_religion.md", "category": "mythology"},
    {"title": "Valhalla", "filename": "valhalla.md", "category": "mythology"},
    {"title": "Odin", "filename": "odin.md", "category": "mythology"},
    {"title": "Seeress (Germanic)", "filename": "volva.md", "category": "mythology"},
    {"title": "Norse rituals", "filename": "norse_rituals.md", "category": "mythology"},
    {"title": "Blót", "filename": "blot.md", "category": "mythology"},
    {"title": "Norse funeral", "filename": "norse_funeral.md", "category": "mythology"},
    {"title": "Viking Age arms and armour", "filename": "viking_age_arms_and_armour.md", "category": "mythology"},
    {"title": "Longship", "filename": "longship.md", "category": "mythology"}
]


def fetch_article(title: str) -> dict:
    """Pulls an article using Wikipedia API"""

    # Send request
    params = {"action": "query",
              "prop": "extracts", 
              "explaintext": 1,
              "redirects": 1,
              "format": "json",
              "titles": title}
    
    headers = {"User-Agent": USER_AGENT}

    response = requests.get(WIKIPEDIA_API_URL, params = params, headers = headers, timeout = 15)
    response.raise_for_status()
    payload = response.json()

    # Check payload
    pages = payload.get("query", {}).get("pages", {})
    if not pages:
        raise ValueError(f"No pages returned for '{title}'")

    page = next(iter(pages.values()))
    if "missing" in page:
        raise ValueError(f"Article not found: '{title}'")

    resolved_title = page.get("title", title)
    extract = page.get("extract", "")
    if not extract.strip():
        raise ValueError(f"Empty extract for '{title}' (resolved: '{resolved_title}')")

    page_url = "https://en.wikipedia.org/wiki/" + resolved_title.replace(" ", "_")

    return {"resolved_title": resolved_title, "extract": extract, "url": page_url}


def clean_article(extract: str) -> str:
    """
    Cleans the fetched Wikipedia article:
    - Collapses 3+ blank lines down to 2
    - Strips trailing whitespace per line
    - Drops common boilerplate trailing sections
    """

    boilerplate_sections = ["see also", "references", "external links",
                            "further reading", "notes", "citations", "bibliography"]

    lines = extract.replace("\r\n", "\n").split("\n")
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        heading_match = re.match(r"^=+\s*(.+?)\s*=+$", stripped)
        if heading_match and heading_match.group(1).strip().lower() in boilerplate_sections:
            break
        cleaned_lines.append(line.rstrip())

    text = "\n".join(cleaned_lines)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text


def write_markdown(category: str, article: dict, filename: str) -> Path:
    """Saves the article as a MD file. Use for reviewing/spot-checking corpus"""

    # Get retrieved date and cleaned article
    retrieved_date = date.today().isoformat()
    body = clean_article(article["extract"])

    # Build the Markdown
    header = (f"# {article['resolved_title']}\n\n"
              f"- **Source:** Wikipedia\n"
              f"- **URL:** {article['url']}\n"
              f"- **Category:** {category}\n"
              f"- **Retrieved:** {retrieved_date}\n"
              f"- **License:** {LICENSE_NOTE}\n\n"
              f"---\n\n")
    content = header + body + "\n"

    # Save Markdown
    out_path = RAW_DIR / filename
    out_path.write_text(content, encoding="utf-8")
    return out_path


def write_json(category: str, article: dict, filename: str) -> Path:
    """Saves the article as a JSON file"""

    # Get retrieved date and cleaned article
    retrieved_date = date.today().isoformat()
    body = clean_article(article["extract"])

    # Build the JSON
    record = {"title": article["resolved_title"],
              "source": "Wikipedia",
              "url": article["url"],
              "category": category,
              "retrieved": retrieved_date,
              "license": LICENSE_NOTE,
              "text": body}

    # Save JSON
    json_filename = Path(filename).with_suffix(".json").name
    out_path = RAW_DIR / json_filename
    out_path.write_text(json.dumps(record, ensure_ascii = False, indent = 2), encoding = "utf-8")
    return out_path


def main():
    RAW_DIR.mkdir(parents = True, exist_ok = True)
    successes = []
    failures = []

    # Fetch and save each article
    for article in ARTICLES:
        title = article["title"]
        filename = article["filename"]
        category = article["category"]

        print(f"Fetching '{title}'...")
        try:
            fetched_article = fetch_article(title)
            # md_path = write_markdown(category, fetched_article, filename)
            json_path = write_json(category, fetched_article, filename)

            successes.append(filename)
            print(f"  SUCCESS: retrieved {fetched_article['resolved_title']}")
        except Exception as e:
            failures.append((title, str(e)))
            print(f"  FAILED: could not retrieve '{title}'")

        # Pause for a few seconds before making the next request
        time.sleep(10)

    print("\n--- SUMMARY ---")
    print(f"Succeeded: {len(successes)} / {len(ARTICLES)}")
    if failures:
        print("Failed:")
        for title, error in failures:
            print(f"  - {title}: {error}")


if __name__ == "__main__":
    main()
