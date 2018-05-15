
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import pandas as pd
import requests
from splinter import Browser


# In[2]:


def init_browser():
    executable_path = {"executable_path":"/Users/Zachk/Desktop/chromedriver.exe"}
    return Browser('chrome', **executable_path,headless=False)

    


# In[3]:


url_1 = 'https://mars.nasa.gov/news/'
url_2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
url_3 = 'https://twitter.com/marswxreport?lang=en'
url_4 = 'http://space-facts.com/mars/'
url_5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


    
# In[4]:
def scrape():
    browser=init_browser()
    browser.visit(url_1)
    title= browser.find_by_css('.content_title').first.text
    news= browser.find_by_css('.article_teaser_body').first.text



# In[5]:


    browser=init_browser()
    browser.visit(url_2)
    browser.find_by_id('full_image').click()
    featured_image=browser.find_by_css('.fancybox-image').first['src']



# In[6]:


    browser=init_browser()
    browser.visit(url_3)
    for text in browser.find_by_css('.tweet-text'):
        if text.text.partition(" ")[0] == 'Sol':
            weather = text.text
        break
    




# In[7]:


    df= pd.read_html(url_4, attrs = {'id': 'tablepress-mars'})[0]
    df = df.set_index(0).rename(columns={1:'value'})
    del df.index.name
    facts = df.to_html()
   


# In[8]:


    hemispheres= requests.get(url_5)
    soup= BeautifulSoup(hemispheres.text,"html.parser")
    hemisphere_list = soup.find_all('a', class_= "itemLink product-item")



# In[10]:


    hemisphere_img = []
    for img in hemisphere_list:
        img_title = img.find('h3').text
        link = "https://astrogeology.usgs.gov/" + img["href"]
        img_request= requests.get(link)
        soup_= BeautifulSoup(img_request.text, 'html.parser')
        img_tag= soup_.find('div',class_='downloads')
        img_url= img_tag.find('a')['href']
        hemisphere_img.append({"Title":img_title, "Url": img_url})



Mars_scrape = {
    "News_Title":title,
    "Paragraph_Text":news,
    "Mars_Image": featured_image,
    "Mars_Weather":weather,
    "Mars_Facts":facts,
    "Mars_Hemisphere":hemisphere_img
}