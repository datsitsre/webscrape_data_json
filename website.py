import scrape_api


url = "https://malawi24.com/"

scrape_api.scrape_and_save(url, "my_data_data_new_test.json")


clean_data_out = scrape_api.clean_data("datasets/", "data.json")

#print(clean_data_out)

database_insert = scrape_api.insert_into_database(clean_data_out)
print(database_insert)
#data = scrape_api.scrape_website(url)
#scrape_api.save_to_json(data, "my_data.json")