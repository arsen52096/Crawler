__author__ = 'arsen52096'

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import datetime




def get_links_RBK(url, no_of_pagedowns, path_of_webdriver):
    
    browser = webdriver.Chrome(path_of_webdriver)
    browser.get(url)
    time.sleep(1)
    elem = browser.find_element_by_tag_name('body')
    
    while no_of_pagedowns:
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)
        no_of_pagedowns-=1
        
    html_source = browser.page_source
    soup = BeautifulSoup(html_source, 'html.parser')
    
    links = []
    
    try:
        for item in range(len(soup.find('div', {'class': 'l-row js-search-container'}).find_all('a'))):
            links.append(soup.find('div', {'class': 'l-row js-search-container'}).find_all('a')[item].get('href'))
    except:
        links.append('None')
 
    return links



def date_month():
    date = datetime.datetime.strptime(
        str(datetime.datetime.today())[5:10], '%m-%d'
    ).strftime('%d %B')
    
    return date+', '


def clear_str(s):
    s = s.replace('\xa0', ' ')
    s = s.replace('\n', '')
    s = s.replace('u200b', ' ')
    return s


def extract_all(links):
    
    date_list = []
    genre_list = []
    article_title_list = []
    body_list = []
    
    
    for i in range(len(links)):
        if links[i] != 'None':
            link = links[i]
            page = requests.get(link)
            soup = BeautifulSoup(page.content, 'html.parser')
        
        
            try:
                date = clear_str(soup.find(attrs={'class' : 'article__header__date'}).text)
                if len(date) == 5:
                    date = date_month()+' '+date
                    date = date.replace('February', 'февр')
                    date_list.append(date)
                else:
                    date_list.append(date)
            except:
                date_list.append('No date')
        
        
            try:
                genre = clear_str_genre(soup.find(attrs={'class' : 'article__header__category'}).text)
                genre = genre.replace(',', '')
                genre_list.append(genre)
            except:
                genre_list.append('Жанр не указан')
            
            article_title = clear_str(soup.find(attrs={'class' : 'article__header__title'}).text)
            article_title_list.append(article_title)


        
            try:
                text = ''
                for p in soup.find_all('p'):
                    if not p.has_attr('class'):
                        text += p.text.strip() + ' '
                body_list.append(clear_str(text))
            except:
                body_list.append('No text')
            
        
            
    data_lenta = {
        'Date': date_list,
        'genre': genre_list,
        'title': article_title_list,
        'article_test': body_list,
    }
        
    
    return data_lenta


if __name__ == '__main__':
	
	url = 'https://www.rbc.ru/tags/?query=РБК&project=rbcnews'
	no_of_pagedowns = 10
	path_of_webdriver = 'c:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe'


	general_dataframe = pd.DataFrame(
        extract_all(get_links_RBK(url, no_of_pagedowns, path_of_webdriver))
            )[['Date', 'genre', 'title', 'article_test']]

	writer = pd.ExcelWriter('RBC.xlsx')
	general_dataframe.to_excel(writer)
	writer.save()