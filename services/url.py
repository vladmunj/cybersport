from urllib.parse import urlsplit


def extract_match_id(url: str) -> int:
    path = urlsplit(url).path
    match_id = path.rstrip("/").split("/")[-1]
    if not match_id.isdigit(): raise ValueError(f"Invalid match URL: {url}")
    return int(match_id)

def extract_event_slug(url: str) -> str:
    path = urlsplit(url).path
    event_slug = path.rstrip("/").split("/")[-1].replace("-", "_")
    return event_slug