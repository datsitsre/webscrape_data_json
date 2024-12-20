from scrape_api import scrape_and_save, clean_data, insert_into_database


url = "https://malawi24.com/"
filename_store_json = "datasets/stored.json"

#Scrape the data
scrape_and_save(url, filename_store_json)

#Clean the data
clean_data_out = clean_data("datasets/", "stored.json")

#Insert the data into the database
insert_into_database(clean_data_out)