import requests

def fetch_url(url: str) -> str:
    """Fetch content from URL, handling GitHub URLs specially."""
    if "github.com" in url and "/blob/" in url:
        url = url.replace("github.com", "raw.githubusercontent.com")
        url = url.replace("/blob/", "/")
    
    response = requests.get(url)
    response.raise_for_status()
    return response.text 