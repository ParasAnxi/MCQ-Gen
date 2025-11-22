import requests
from bs4 import BeautifulSoup


def process_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        for script in soup(["script", "style", "header", "footer", "nav"]):
            script.decompose()
        return soup.get_text(separator="\n")
    except Exception as e:
        print(f"Error processing URL: {e}")
        return ""
