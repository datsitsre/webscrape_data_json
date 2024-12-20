from bs4 import BeautifulSoup
import requests



url = "https://malawi24.com"
try:
    headers = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

except requests.RequestException as ex:
    print({"error": f"Failed to fetch the webpage: {str(ex)}"})

    

soup = BeautifulSoup(response.text, "html.parser")

data = {
    "content":
        [
            {
                "images": [img.get('src') for img in soup.find_all('img')],
                "title": [a.text.strip() for a in soup.find_all("a")],
                "content": [cont.text.strip() for cont in soup.find_all("div", class_="excerpt")],
                "link": [a.get('href') for a in soup.find_all('a') if a.get('href')]
            }
        ]
}

print(data)