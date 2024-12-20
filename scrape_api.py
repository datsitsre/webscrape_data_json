import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
#import numpy as np
import pandas as pd
import mysql.connector 
#from datetime import date


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
    }

    
    return data


def save_to_json(data, filename, indent=2):
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
        

def scrape_and_save(url, filename_stored_json):
    """
    Convenience function to scrape a website and save to JSON in one step.
    
    Parameters:
    url (str): The URL to scrape
    filename (str): Name of the output JSON file
    """
    data = scrape_website(url)
    save_to_json(data, filename_stored_json)
    return data

    
    
def clean_data(path, filename):
    """
      Path : The path of file
      filename : The filename of file
    """
    try:
        with open(path + filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            images_df =  data['content']['content'][0]['images']
            title_series = data['content']['content'][0]['title']
            content_series = data['content']['content'][0]['content']
            link_series = data['content']['content'][0]['link']
            #scraped_date =  data['metadata']['timestamp']
            #url = data['metadata']['url']

            #remove title and date from title data
            title_series = [title_series[data] for data in range(len(title_series)) if title_series[data] not in 
                            ["", "0", "1","...", "Dec 18, 2024", "Dec 16, 2024", 
                             "Dec 11, 2024", "Dec 14, 2024", "Dec 17, 2024", "Dec 14, 2024",
                             "Dec 16, 2024", "Jan 19, 2021","Apr 08, 2024","Apr 08, 2024", 
                             "Nov 30, 2024","Jan 31, 2024", "Oct 30, 2024", "Aug 27, 2020", 
                             "Aug 27, 2020", "'Dec 15, 2024", "Dec 15, 2024", "Jan 31, 2024", 
                             "Oct 04, 2024", "Nov 30, 2024"]]
            #remove white space
            content_series = [n.rstrip('...').strip(' ') for n in content_series]

            #remove /
            link_series = [a for a in link_series if a not in ['/']]

            #convert data into a series 
            images_sf = pd.Series(images_df)
            link_sf = pd.Series(link_series)
            title_sf = pd.Series(title_series)
            content_sf = pd.Series(content_series)

            
            #remove duplicate datasets
            images_sf = images_sf.drop_duplicates()
            link_sf = link_sf.drop_duplicates()
            title_sf = title_sf.drop_duplicates()
            content_sf = content_sf.drop_duplicates()

            
            #store in json file
            data_df = {
                        'image' :  images_sf.tolist(),
                        'link' : link_sf.tolist(),
                        'title' : title_sf.tolist(),
                        'content' : content_sf.tolist(),
                    }

            return data_df
    except Exception as e:
        print("Error data")







def insert_into_database(data: dict):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='test_db',
            user='user',
            password='user')
        cursor = connection.cursor()

        keys = data.keys()
        values = list(zip(*data.values()))

        table_name = 'articles'

        columns = ", ".join(keys)
        placeholders = ", ".join(["%s"] * len(keys))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        cursor.executemany(query, values)
        connection.commit()

    except  mysql.connector.Error as error:
        print("Error connecting to database {}".format(error))