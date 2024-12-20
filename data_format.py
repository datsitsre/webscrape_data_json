from matplotlib import pyplot
import numpy as np

import pandas as pd
import re
import json



# open the file 

with open('datasets/data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    

#read data
#df = pd.DataFrame.from_dict(data['content']['content'][0])

#df


# clean each columns
images_df =  data['content']['content'][0]['images']
title_series = data['content']['content'][0]['title']
content_series = data['content']['content'][0]['content']
link_series = data['content']['content'][0]['link']


#clean the title series
"""
for n in range(len(title_series)):
    if title_series[n] in ["","0", "1", "..."]:
        print(title_series[n])
    #   title_series.pop(n) 
    #print(title_series[n])
"""

#title_series = [title_series[data] for data in range(len(title_series)) if title_series[data] not in ["", "0", "1","...", "Dec 18, 2024", "Dec 16, 2024", "Dec 11, 2024", "Dec 14, 2024", "Dec 17, 2024", "Dec 14, 2024", "Dec 16, 2024", "Jan 19, 2021","Apr 08, 2024","Apr 08, 2024", "Nov 30, 2024","Jan 31, 2024", "Oct 30, 2024", "Aug 27, 2020", "Aug 27, 2020", "'Dec 15, 2024", "Dec 15, 2024", "Jan 31, 2024", "Oct 04, 2024", "Nov 30, 2024"]]
#for a in range(len(title_series)):
#    if title_series[a] in ["Dec 18, 2024"]:
#       print(title_series[a])

#print(title_series)

#print(images_df)
#print(len(images_df))
#print(len(title_series))
#print(len(link_series))

#
#print(content_series)

#link_series = [a for a in link_series if a not in ['/']]
#print(link_series)


#length
#print(f"The lenght of images {len(images_df)}")
#print(f"The lenght of link {len(link_series)}")
#print(f"The lenght of title {len(title_series)}")
#print(f"The lenght of content {len(content_series)}")

### Series
images_sf = pd.Series(images_df)
link_sf = pd.Series(link_series)
title_sf = pd.Series(title_series)
content_sf = pd.Series(content_series)

#print(images_sf)
#print(link_sf)
#print(title_sf)
#print(content_sf)

#print("""
      
#     Removed data 
      
#      """)
#remove duplicated
images_sf = images_sf.drop_duplicates()
link_sf = link_sf.drop_duplicates()
title_sf = title_sf.drop_duplicates()
content_sf = content_sf.drop_duplicates()

#print(f"The lenght of images {len(images_df)}")
#print(f"The lenght of link {len(link_series)}")
#print(f"The lenght of title {len(title_series)}")
#print(f"The lenght of content {len(content_series)}")


#print(images_sf)
#print(link_sf)
#print(title_series)
#print(content_sf)


#store data in json file
data_df = {
    'images_sf' :  images_sf.tolist(),
    'link_sf' : link_sf.tolist(),
    'title_sf' : title_sf.tolist(),
    'content_sf' : content_sf.tolist()
}

print(data_df)