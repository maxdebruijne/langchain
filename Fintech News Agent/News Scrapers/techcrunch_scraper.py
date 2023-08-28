import pandas as pd
import requests
from bs4 import BeautifulSoup



# class TechCrunchScraper():

    
#     def __init__(self):
#         self.baseurl = 'https://www.techcrunch.com/'



base_url = 'https://www.techcrunch.com/'
page = requests.get(base_url)
soup = BeautifulSoup(page.content, "html.parser")
link = soup.find_all('a', {'class':'post-block__title__link'})
for item in link:
    print(item)

