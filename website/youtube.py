from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd

def get_driver():
  options = Options()
  options.add_argument('--headless')
  options.add_argument('--no-sandbox')
  options.add_argument('--single-process')
  options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome('D:\chromedriver\chromedriver.exe',options=options)
  return driver

def youtube(search):
    youtube_url='https://www.youtube.com/results?search_query='
    youtube_url=youtube_url+search
    youtube_url=youtube_url+'&sp=EgIQAw%253D%253D'
    driver=get_driver()
    driver.get(youtube_url)
    
    VIDEO_DIV_TAG = 'ytd-playlist-renderer'
    videos = driver.find_elements(By.TAG_NAME, VIDEO_DIV_TAG)
    print(len(videos))
    
    ch_title=[]
    ch_url=[]
    ch_thumbnail=[]
    ch_name=[]

    for i in range(len(videos)):
        if i==16:
            break
        video=videos[i]
        title_tag = video.find_element(By.ID,'video-title')
        title = title_tag.text.encode("utf-8")
        ch_title.append(title)
        
        channel_url=video.find_element(By.ID,'thumbnail')
        url =channel_url.get_attribute('href')
        ch_url.append(url)
        
        thumbnail_tag = video.find_element(By.TAG_NAME, 'img')
        thumbnail_url = thumbnail_tag.get_attribute('src')
        ch_thumbnail.append(thumbnail_url)
        
        channel_div = video.find_element(By.CLASS_NAME, 'ytd-channel-name')
        channel_name = channel_div.text.encode("utf-8")
        ch_name.append(channel_name)
    
    topics_dict={
        'title':ch_title,
        'channel-name':ch_name,
        'link':ch_url,
        'photo':ch_thumbnail
        }
    topics_df=pd.DataFrame(topics_dict)
    name='data\youtube\\'+search+'.csv'
    topics_df.to_csv(name,index=None)
    
    driver.close()
    driver.quit()

    return topics_dict