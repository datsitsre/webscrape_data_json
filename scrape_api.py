import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime


def scrape_website(url):
    """
     Scrape a website and extract basic information using BeautifulSoup.
     
     Parameters
     url (str): The URL of the website to scrape
     
     Returns:
     dict: Dictionary containing extracted data
    """

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

    except requests.RequestException as ex:
        return {"error": f"Failed to fetch the webpage: {str(ex)}"}

    
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    
    # Extract data
    data = {
        "metadata": {
            "url": url,
            "timestamp": datetime.now().isoformat(),
            "status_code": response.status_code
        },
        "content": {
            "title": soup.title.string if soup.title else "No title found",
            "headings": {
                "h1": [h.text.strip() for h in soup.find_all('h1')],
                "h2": [h.text.strip() for h in soup.find_all('h2')],
                "h3": [h.text.strip() for h in soup.find_all('h3')]
            },
            "paragraphs": [p.text.strip() for p in soup.find_all('p')],
            "links": [
                {
                    "text": a.text.strip(),
                    "href": a.get('href'),
                    "title": a.get('title', '')
                } for a in soup.find_all('a') if a.get('href')
            ],
            "images":
                [
                    {
                        "alt": img.get('alt', ''),
                        "src": img.get('src'),
                        "title": img.get('title', '')
                    } for img in soup.find_all('img')
                ]
        }
    }

    
    return data


def save_to_json(data, filename="scraped_data.json", indent=2):
    """
    Save the scraped data to a JSON file.
    
    
    Parameters:
    dat (dict): The scraped data
    filename (str): Name of the JSON file
    indent (int): Number of spaces for indentation in the JSON file
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving to JSON: {str(e)}")

        

def scrape_and_save(url, filename="scraped_data.json"):
    """
    Convenience function to scrape a website and save to JSON in one step.
    
    Parameters:
    url (str): The URL to scrape
    filename (str): Name of the output JSON file
    """
    data = scrape_website(url)
    save_to_json(data, filename)
    return data