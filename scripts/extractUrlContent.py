import requests
from bs4 import BeautifulSoup

def extractUrlContent(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract the text content from the HTML
    text_content = soup.get_text(separator=' ', strip=True)
    
    print(text_content)
    
    return text_content
