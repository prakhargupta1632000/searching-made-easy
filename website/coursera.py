from numpy import append
import requests
from bs4 import BeautifulSoup
import pandas as pd

def result2(search):
    topic_url='https://www.coursera.org/browse/data-science/'
    topic_url=topic_url+search
    response=requests.get(topic_url)
    name = response.status_code
    page_contents=response.text
    doc=BeautifulSoup(page_contents,'html.parser')
    topic_link_tags=doc.find_all('a',{'class':'nostyle collection-product-card'})
    topic_urls=[]
    for tag in topic_link_tags:
        topic_urls.append('https://www.coursera.org'+tag['href'])
    topic_tutor=[]
    topic_titles=[]
    topic_image=[]
    topic_ratings=[]
    topic_time=[]
    topic_cost=[]
    for url in topic_urls:
        topic_url=url
        response=requests.get(topic_url)
        page_contents=response.text
        doc=BeautifulSoup(page_contents,'html.parser')
        selection_class1='banner-title banner-title-without--subtitle m-b-0'
        selection_class2='banner-title m-b-0'
        topic_title_tags=doc.find_all('h1',{'class':[selection_class1,selection_class2]})
        tutor_class1='_1g3eaodg'
        tutor_class2='_69gnimg'
        topic_tutor_tags=doc.find_all('img',{'class':[tutor_class1,tutor_class2]})
        topic_image_tags=doc.find_all('img',{'class':['_1g3eaodg','_69gnimg']})
        topic_rating_tags=doc.find_all('span',{'class':'_16ni8zai m-b-0 rating-text number-rating number-rating-expertise'})
        for tag in topic_title_tags:
            topic_titles.append(tag.text)
        for tag in topic_tutor_tags:
            topic_tutor.append(tag['title'])
        for tag in topic_image_tags:
            topic_image.append(tag['src'])
        for tag in topic_rating_tags:
            topic_ratings.append(tag.text)
        detail_class1='_16ni8zai m-b-0'
        detail_class2='_16ni8zai m-b-0 m-t-1s'
        topic_detail_tags=doc.find_all('div',{'class':[detail_class1,detail_class2]})
        f=0
        for tag in topic_detail_tags:
            if(tag.text[:6]=='Approx' or tag.text[-5:]=='hours'):
                topic_time.append(tag.text)
                f=f+1
                break
        if f==0:
             topic_time.append('NIL')
        topic_cost.append('NIL')
    topics_dict={
    'title':topic_titles[:18],
    'tutor':topic_tutor[:18],
    'cost':topic_cost[:18],
    'time':topic_time[:18],
    'rating':topic_ratings[:18],
    'url':topic_urls[:18],
    'image':topic_image[:18]
    }
    topics_df=pd.DataFrame(topics_dict)
    name='data\coursera\\'+search+'.csv'
    topics_df.to_csv(name,index=None)


def coursera(search): 
    topic_url='https://www.coursera.org/courses?query='
    f=0
    for i in range(len(search)):
        if search[i]=='-':
            f=f+1
            break
    if f==0:
        topic_url=topic_url+search
    if f!=0:
        topic_url=topic_url+search[:i]
        topic_url=topic_url+'%20'
        topic_url=topic_url+search[i+1:]
    response=requests.get(topic_url)
    name = response.status_code
    page_contents=response.text
    doc=BeautifulSoup(page_contents,'html.parser')
    selection_class='cds-7 card-title css-cru2ji cds-9'
    topic_title_tags=doc.find_all('h2',{'class':selection_class})
    tutor_class='cds-7 partner-name css-1cxz0bb cds-9'
    topic_tutor_tags=doc.find_all('span',{'class':tutor_class})
    topic_link_tags=doc.find_all('a',{'class':'result-title-link'})
    topic_image_tags=doc.find_all('img',{'class':'product-photo'})
    topic_rating_tags=doc.find_all('span',{'class':'ratings-text'})
    topic_titles=[]
    for tag in topic_title_tags:
        topic_titles.append(tag.text)
    if len(topic_titles)==0:
        result2(search)
        return
    topic_tutors=[]
    for tag in topic_tutor_tags:
        topic_tutors.append(tag.text.strip())
    topic_urls=[]
    for tag in topic_link_tags:
        topic_urls.append('https://www.coursera.org'+tag['href'])
    topic_image=[]
    for tag in topic_image_tags:
        topic_image.append(tag['src'])
    while len(topic_image)!=len(topic_titles):
        topic_image.append('https://akm-img-a-in.tosshub.com/indiatoday/images/story/201810/stockvault-person-studying-and-learning---knowledge-concept178241_0.jpeg?yCXmhi7e2ARwUtzHHlvtcrgETnDgFwCK&size=770:433')
    topic_rating=[]
    for tag in topic_rating_tags:
        topic_rating.append(tag.text)
    topic_time=[]
    topic_cost=[]
    for url in topic_urls:
        topic_url=url
        response=requests.get(topic_url)
        page_contents=response.text
        doc=BeautifulSoup(page_contents,'html.parser')
        detail_class1='_16ni8zai m-b-0'
        detail_class2='_16ni8zai m-b-0 m-t-1s'
        detail_class3='cds-105 css-1xf7jx1 cds-107'
        topic_detail_tags=doc.find_all(['div','span'],{'class':[detail_class1,detail_class2,detail_class3]})
        f=0
        for tag in topic_detail_tags:
            if(tag.text[:6]=='Approx' or tag.text[-5:]=='hours'):
                topic_time.append(tag.text)
                f=f+1
                break
        if f==0:
             topic_time.append('NIL')
        # cost_class='rc-ReactPriceDisplay'
        # topic_cost_tags=doc.find_all('span',{'class':cost_class})
        # for tag in topic_cost_tags:
        topic_cost.append('NIL')

    topics_dict={
    'title':topic_titles[:18],
    'tutor':topic_tutors[:18],
    'cost':topic_cost[:18],
    'time':topic_time[:18],
    'rating':topic_rating[:18],
    'url':topic_urls[:18],
    'image':topic_image[:18]
    }
    topics_df=pd.DataFrame(topics_dict)
    name='data\coursera\\'+search+'.csv'
    topics_df.to_csv(name,index=None)
    return topics_dict

#add cost instead of 'NIL'
#image link after 5 images not coming
#two cost was not coming (new ta courses)