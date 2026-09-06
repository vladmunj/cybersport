from urllib.parse import urlsplit


def extract_match_id(url: str) -> int:
    path = urlsplit(url).path
    match_id = path.rstrip("/").split("/")[-1]
    if not match_id.isdigit(): raise ValueError(f"Invalid match URL: {url}")
    return int(match_id)