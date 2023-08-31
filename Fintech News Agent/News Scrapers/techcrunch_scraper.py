import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import json

# class TechCrunchScraper():

    
#     def __init__(self):
#         self.baseurl = 'https://www.techcrunch.com/'



base_url = 'https://www.techcrunch.com/'
page = requests.get(base_url)
soup = BeautifulSoup(page.content, "html.parser")



def get_article_links_and_title(soup):
    "This function gets all the different links of the latest articles on TechCrunch."
    titles, links = [], []
    link = soup.find_all('a', {'class':'post-block__title__link'})
    for item in link[2:]:
        links.append(item['href'])
        titles.append(item.get_text().strip())
    return links, titles


def get_article_authors_and_dates(soup):
    """This function gets the article and dates of the latest published articles on TechCrunch."""
    date_tags = soup.find_all('time')
    dates = [date_tag.get_text().strip() for date_tag in date_tags]
    author_tags = soup.find_all('span', class_='river-byline__authors')
    authors = [author.get_text().strip() for author in author_tags]

    return authors, dates


def get_article_context(soup):
    "This function gets all the context from the given article."
    article_context = soup.select_one('div.article-content')
    return "\n".join([x.get_text() for x in article_context.find_all('p')])


def main():
    article_contexts = []
    article_links, article_titles = get_article_links_and_title(soup)
    article_authors, article_dates = get_article_authors_and_dates(soup)
    for link in article_links:
        page2 = requests.get(link)
        soup2 = BeautifulSoup(page2.content, "html.parser")
        article_contexts.append(get_article_context(soup2))
    
    descriptions =[{'Date': date, 'Author':author, 'Link':link, 'Context':context} for date, author, link, context in zip(article_authors, article_dates, article_links, article_contexts)]
    techcrunch_articles = {title: d for title, d in zip(article_titles, descriptions)}
    json_object = json.dumps(techcrunch_articles, indent = 4) 

    print(techcrunch_articles)

    # with open('TechCrunch_Dictionary', 'w') as f:
    #     f.write(techcrunch_articles)

    

if __name__ == '__main__':
    main()
