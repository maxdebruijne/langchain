import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import json

class TechCrunchScraper():

    
    def __init__(self):
        self.base_url = 'https://www.techcrunch.com/'
        self.page = requests.get(self.base_url)
        self.soup = BeautifulSoup(self.page.content, "html.parser")



    def get_article_links_and_title(self, soup):
        "This function gets all the different links of the latest articles on TechCrunch."
        titles, links = [], []
        link = soup.find_all('a', {'class':'post-block__title__link'})
        for item in link[2:]:
            links.append(item['href'])
            titles.append(item.get_text().strip())
        return links, titles


    def get_article_authors_and_dates(self, soup):
        """This function gets the article and dates of the latest published articles on TechCrunch."""
        date_tags = soup.find_all('time')
        dates = [date_tag.get_text().strip() for date_tag in date_tags]
        author_tags = soup.find_all('span', class_='river-byline__authors')
        authors = [author.get_text().strip() for author in author_tags]

        return authors, dates


    def get_article_context(self, soup):
        "This function gets all the context from the given article."
        article_context = soup.select_one('div.article-content')
        return "\n".join([x.get_text() for x in article_context.find_all('p', class_=False)])


    def get_article_type_and_category(self, soup):
        ""
        if soup.find('div', class_='extra-crunch-offer-container') != None:
            article_type = 'This is a Premium Article, and therefore only displays the first part of the article.'
        else:
            article_type = 'This is a Free Article.'

        meta_tag = soup.find('meta', {'property': 'mrf:tags'}).get('content').split(';')
        for tag in meta_tag:
            if 'Primary Category' in tag:
                primary_category = tag.split(':')[-1].strip()
        return article_type, primary_category


    def write_unique_new_articles_to_text_and_json(self, techcrunch_dict_file, techcrunch_text_file, techcrunch_articles):
        ""
        with open(techcrunch_dict_file, 'r') as f:
            existing_data = json.load(f)

        merged_dict = {**existing_data, **techcrunch_articles}
        
        with open(techcrunch_dict_file, 'w') as f:
            json.dump(techcrunch_articles, f)

        with open(techcrunch_text_file, 'w') as f:
            f.write(f"Total number of articles: {len(merged_dict)}")
            for key, dict_ in merged_dict.items():
                f.write(f"\n\nDate: {dict_['Date']}\nAuthor: {dict_['Author']}\nCategory: {dict_['Category']}\nType: {dict_['Type']}\nLink: {dict_['Link']}\nTitle: {key}\nContext: {dict_['Context']}\n")
        


    def main(self):
        article_contexts, article_types, primary_categories = [], [], []
        article_links, article_titles = self.get_article_links_and_title(self.soup)
        article_authors, article_dates = self.get_article_authors_and_dates(self.soup)
        for link in article_links:
            page2 = requests.get(link)
            soup2 = BeautifulSoup(page2.content, "html.parser")
            article_contexts.append(self.get_article_context(soup2))

            article_type, primary_category = self.get_article_type_and_category(soup2)
            article_types.append(article_type)
            primary_categories.append(primary_category)
        
        descriptions =[{'Date': date, 'Author':author, 'Category':category, 'Type':type_, 'Link':link, 'Context':context} for date, author, category, type_, link, context in zip(article_dates, article_authors, primary_categories, article_types, article_links, article_contexts)]
        techcrunch_articles = {title: d for title, d in zip(article_titles, descriptions)}

        techcrunch_dict_file = '/Users/maxdebruijne/Documents/GitHub/langchain/Fintech News Agent/Data/TechCrunch_Dictionary.json'
        techcrunch_text_file = '/Users/maxdebruijne/Documents/GitHub/langchain/Fintech News Agent/Data/TechCrunch_Articles.text'
        self.write_unique_new_articles_to_text_and_json(techcrunch_dict_file, techcrunch_text_file, techcrunch_articles)

    

if __name__ == '__main__':
    scraper = TechCrunchScraper()
    scraper.main()
