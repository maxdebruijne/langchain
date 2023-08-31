import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone


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
        titles.append(item.text)
    return links, titles


def get_article_author_and_time(soup):
    "This function gets the author and time of a given article, when provided with soup object."
    authors, times = [], []
    time_tags = soup.find_all('time', class_ = 'full-date-time')
    author_tag = soup.select_one('div.article__byline').find('a').get_text().strip()
    print(time_tags)
    for time in time_tags:
        raw_datetime = time['datetime']
        raw_datetime = datetime.strptime(raw_datetime, '%Y-%m-%dT%H:%M:%S%z').astimezone()
        final_datetime = raw_datetime.strftime('%I:%M %p %Z %B %d, %Y')
        times.append(final_datetime)
    # for author in author_tag.find_all('a'):
        # authors.append(author.get_text().strip())
    return times, authors


def get_article_context(soup):
    "This function gets all the context from the given article."
    article_context = soup.select_one('div.article-content')
    print("\n".join([x.get_text() for x in article_context.find_all('p')]))
    print('-------------------------------')




article_links, article_titles = get_article_links_and_title(soup)


for link in article_links:
    page2 = requests.get(link)
    soup2 = BeautifulSoup(page2.content, "html.parser")
    times, authors = get_article_author_and_time(soup2)
    get_article_context(soup2)