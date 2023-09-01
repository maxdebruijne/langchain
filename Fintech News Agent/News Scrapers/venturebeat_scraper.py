import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import json

class VentureBeatScraper():

    
    def __init__(self):
        self.base_url = 'https://www.venturebeat.com/'
        self.page = requests.get(self.base_url)
        self.soup = BeautifulSoup(self.page.content, "html.parser")


    def get_article_link_and_title(self, soup):
        "This function returns the link and title of all articles on main page VB."
        article_tag = self.soup.find_all('article', class_ = 'ArticleListing')
        links = [link.find('a')['href'] for link in article_tag]
        titles = [title.find('a')['title'].replace("'Permalink to ", "") for title in article_tag]
        return links, titles


    def get_article_author(self, soup):
        "This function returns the author of a VB article."
        author = soup.find('div', class_='Article__author-info').find('a').get_text()
        if author =='Business Wire':
            author = 'Press Release'
        return author
    
    
    def get_article_date(self, soup):
        "This function returns the date of a VB article."
        date = soup.find('div', class_='article-time-container').find('time').get_text()
        return date


    def get_article_content(self, links):
        "This function uses all the different links (as list) to get the content of each article."
        contents, authors, dates = [], [], []
        for link in links:
            page = requests.get(link)
            soup = BeautifulSoup(page.content, 'html.parser')
            content_tag = soup.find('div', class_ = 'article-content').findChildren('p', recursive=False)
            contents.append("\n".join([x.get_text() for x in content_tag]))
            authors.append(self.get_article_author(soup))
            dates.append(self.get_article_date(soup))

        return contents, authors, dates


    def write_unique_new_articles_to_text_and_json(self, venturebeat_dict_file, venturebeat_text_file, venturebeat_articles):
        ""
        with open(venturebeat_dict_file, 'r') as f:
            existing_data = json.load(f)

        merged_dict = {**existing_data, **venturebeat_articles}
        
        with open(venturebeat_dict_file, 'w') as f:
            json.dump(merged_dict, f)

        with open(venturebeat_text_file, 'w') as f:
            f.write(f"Total number of articles: {len(merged_dict)}")
            for key, dict_ in merged_dict.items():
                f.write(f"\n\nDate: {dict_['Date']}\nAuthor: {dict_['Author']}\nLink: {dict_['Link']}\nTitle: {key}\nContent: {dict_['Content']}\n")
        

    def main(self):

        links, titles = self.get_article_link_and_title(self.soup)
        contents, authors, dates = self.get_article_content(links)

        descriptions =[{'Date': date, 'Author':author, 'Link':link, 'Content':content} for date, author, link, content in zip(dates, authors, links, contents)]
        venturebeat_articles = {title: d for title, d in zip(titles, descriptions)}
        
        venturebeat_dict_file = '/Users/maxdebruijne/Documents/GitHub/langchain/Fintech News Agent/Data/VentureBeat_Dictionary.json'
        venturebeat_text_file = '/Users/maxdebruijne/Documents/GitHub/langchain/Fintech News Agent/Data/VentureBeat_Articles.text'
        self.write_unique_new_articles_to_text_and_json(venturebeat_dict_file, venturebeat_text_file, venturebeat_articles)

if __name__ == '__main__':
    scraper = VentureBeatScraper()
    scraper.main()