import requests
from bs4 import BeautifulSoup
import pandas as pd

def edx(search): 
    topic_url='https://www.edx.org/learn/'
    topic_url=topic_url+search
    response=requests.get(topic_url)
    name = response.status_code
    page_contents=response.text
    doc=BeautifulSoup(page_contents,'html.parser')
    selection_class='h4 text-black'
    topic_title_tags=doc.find_all('h3',{'class':selection_class})
    tutor_class='text-gray-700 small provider'
    topic_tutor_tags=doc.find_all('div',{'class':tutor_class})
    topic_link_tags=doc.find_all('a',{'class':'discovery-card-link bg-white text-black'})
    topic_image_tags=doc.find_all('img',{'class':'d-card-hero-image'})
    topic_titles=[]
    for tag in topic_title_tags:
        topic_titles.append(tag.text)
    topic_tutors=[]
    for tag in topic_tutor_tags:
        topic_tutors.append(tag.text.strip())
    topic_urls=[]
    for tag in topic_link_tags:
        topic_urls.append('https://www.edx.org'+tag['href'])
    topic_image=[]
    for tag in topic_image_tags:
        topic_image.append(tag['src'])
    topic_time=[]
    topic_cost=[]
    for url in topic_urls:
        topic_url=url
        response=requests.get(topic_url)
        page_contents=response.text
        doc=BeautifulSoup(page_contents,'html.parser')
        time_class='h4 mb-0'
        topic_title_time=doc.find_all('div',{'class':time_class})
        topic_detailes=[]
        for tag in topic_title_time:
            topic_detailes.append(tag.text)
        topic_time.append(topic_detailes[2])
        topic_cost.append(topic_detailes[4])

    topics_dict={
    'title':topic_titles,
    'tutor':topic_tutors,
    'cost':topic_cost,
    'time':topic_time,
    'url':topic_urls,
    'image':topic_image
    }
    topics_df=pd.DataFrame(topics_dict)
    name='data\edx\\'+search+'.csv'
    topics_df.to_csv(name,index=None)
    return topics_dict


#also add paid courses