import requests
from bs4 import BeautifulSoup

def scrape_article_text(url: str) -> str:
    """Scrapes the main text from a news article URL."""
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all paragraph tags - a common way to store article text
        paragraphs = soup.find_all('p')
        
        # Combine the text from all paragraphs
        article_text = ' '.join([p.get_text() for p in paragraphs])
        
        # A simple check to see if we got meaningful content
        if len(article_text) < 200: # Heuristic: too short might be a soft 404 or error page
            return None

        return article_text

    except requests.exceptions.RequestException as e:
        print(f"Error scraping URL {url}: {e}")
        return None