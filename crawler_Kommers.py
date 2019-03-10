author = 'arsen52096'

import requests
from bs4 import BeautifulSoup
import re
import datetime
import pandas as pd


def url_string(date_first_day) -> list:
    
    date_today = datetime.date.today()
    delta = date_today - date_first_day
    
    date_list = [
        date_first_day + datetime.timedelta(
        days = x
    ) for x in range(0, int((re.findall(r'^\w+', str(delta)))[0]))
    ]

    formating_date_list = [
        datetime.datetime.strptime(
            str(date), '%Y-%m-%d'
        ).strftime('%Y-%m-%d')
        for date in date_list
    ]
    
    hour_r = []
    
    for i in range(0, 9):
        hour_exp = '200'+str(i)
        hour_r.append(hour_exp)
    for i in range(10, 24):        
        hour_exp = '20'+str(i)
        hour_r.append(hour_exp)

    part_of_url = []
    
    for i in formating_date_list:
        for j in hour_r:
            part_of_url.append(i+'%'+j+'%')
            
    urls = []
    
    for i in part_of_url:
        urls.append('https://www.kommersant.ru/ArchiveNew/NewsLazy?regionId=77&date=' + i + '3A59%3A29&extraId=0')    
    
    return urls




def get_links(date_run_url: list)->list:

    links = []
    for date_url in date_run_url:
        page = requests.get(date_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        for link in soup.find(attrs={'class':"archive_date_result__list"}).find_all('a'):
            links.append('https://www.kommersant.ru' + link.get('href'))
        
    links = list(set(links))
    
    return links




def article_text(urls:list) -> dict:
    
    date_list = []
    article_title_list = []
    body_list = []
    
    
    for url in urls:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
    
        date_and_hour = soup.find(attrs={'class': 'title__cake'}).text
        date_list.append(date_and_hour)
    
        article_text = soup.find(attrs={'itemprop' : 'headline'}).text
        article_title_list.append(article_text)
    
        body_text = soup.find(attrs={'class' : 'b-article__text'}).text
        body_list.append(body_text)
    
        data_kommers = {
            'Date': date_list,
            'title': article_title_list,
            'article_test': body_list,
        }
    
    return data_kommers




if __name__ == '__main__':
  
  
  # choose your date of begining 
  date_first_day_kommersant = datetime.date(2019,3,9)

  

  url_strings = url_string(date_first_day_kommersant)
  links = get_links(url_strings)
  data_article = article_text(links)

  general_dataframe = pd.DataFrame(
        data_article)[['Date', 'title', 'article_test']]

  writer = pd.ExcelWriter('kommersant.xlsx')
  general_dataframe.to_excel(writer)
  writer.save()