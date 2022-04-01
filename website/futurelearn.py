import requests
from bs4 import BeautifulSoup
import pandas as pd

def futurelearn(search): 
    topic_url='https://www.futurelearn.com/subjects/it-and-computer-science-courses/'
    topic_url=topic_url+search
    response=requests.get(topic_url)
    name = response.status_code
    page_contents=response.text
    doc=BeautifulSoup(page_contents,'html.parser')
    selection_class='heading-module_wrapper__2dcxt heading-module_sBreakpointAlignmentleft__pCA_Y heading-module_sBreakpointSizemedium__8ELNW heading-module_black__Uge9G heading-module_isCompact__fVqKY'
    topic_title_tags=doc.find_all('h3',{'class':selection_class})
    tutor_class='itemTitle-wrapper_2C5P7 itemTitle-secondary_CSQVr itemTitle-isLight_2ylLM itemTitle-isSmall_1RrJA'
    topic_tutor_tags=doc.find_all('span',{'class':tutor_class})
    topic_link_tags=doc.find_all('a',{'class':'link-wrapper_1GLAu link-withFlexGrow_3346W'})
    topic_image_tags=doc.find_all('img',{'class':'image-module_image__1vzg2 image-module_cover__2_Sai'})
    #topic_rating_tags=doc.find_all('div',{'class':'ReviewStars-text_mSEFD ReviewStars-staticText_3s4UW'})
    topic_time_tags=doc.find_all('p',{'class':'text-module_wrapper__FfvIV text-module_coolGrey__3nOqf text-module_sBreakpointSizexsmall__2Jlmd text-module_sBreakpointAlignmentleft__1MvbB text-module_isRegular__1K97K'})
    topic_titles=[]
    for tag in topic_title_tags:
        topic_titles.append(tag.text)
    topic_tutors=[]
    for tag in topic_tutor_tags:
        topic_tutors.append(tag.text.strip())
    topic_urls=[]
    for tag in topic_link_tags:
        topic_urls.append('https://www.futurelearn.com'+tag['href'])
    topic_image=[]
    i=1
    for tag in topic_image_tags:
        if i%2!=0:
            topic_image.append(tag['src'])
        i=i+1
        
    # topic_rating=[]
    # for tag in topic_rating_tags:
    #     topic_rating.append(tag.text)
    topic_time=[]
    for tag in topic_time_tags:
        if tag.text[-5:]=="weeks":
            topic_time.append(tag.text)
    topic_cost=[]
    for url in topic_urls:
        topic_url1=url
        response=requests.get(topic_url1)
        name1 = response.status_code
        page_contents1=response.text
        doc=BeautifulSoup(page_contents1,'html.parser')
        topic_cost_tags=doc.find_all('span',{'class':['PageHeaderKeyInfoItem-isBold_253Ni','keyInfo-module_content__1K_85']})
        for tag in topic_cost_tags:
            if tag.text!="" and (tag.text[0]=='$' or tag.text[0:2]=='Fr'):
                topic_cost.append(tag.text)
                break

    while len(topic_titles) != len(topic_cost):
        topic_cost.append('NIL')
    while len(topic_titles) != len(topic_time):
        topic_time.append('NIL')
    topics_dict={
    'title':topic_titles,
    'tutor':topic_tutors,
    'cost':topic_cost,
    'time':topic_time,
    'url':topic_urls,
    'image':topic_image
    }
    topics_df=pd.DataFrame(topics_dict)
    name='data\\futurelearn\\'+search+'.csv'
    topics_df.to_csv(name,index=None)

    return topics_dict