#!/usr/bin/env python
# coding: utf-8

# In[2]:


pip install webdriver-manager


# In[3]:


#Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[4]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[5]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
#Optional delay for oading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[6]:


#Setting the HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[7]:


slide_elem.find('div', class_='content_title')


# In[8]:


#Use the parent element to ind the first 'a' tag and save it as 'news_title'
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title                                


# In[9]:


#Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images 

# In[10]:


#Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[11]:


#Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[12]:


#Parse the result html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[13]:


#FInd the relative image url
image_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
image_url_rel


# In[14]:


#Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{image_url_rel}'
img_url


# In[15]:


#Extract the whole table for the galaxyfacts URL
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns =['describe', 'Mars','Earth']
df.set_index('describe', inplace=True)
df


# In[16]:


#converting our dataframe into a html table
df.to_html()


# ### Mars Hemispheres

# In[26]:


browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
html = browser.html
new_soup = soup(html, 'html.parser')
#Searching for hemispheres titles 
hemi_names = []
results = new_soup.find_all('div', class_="collapsible results")
hemispheres = results[0].find_all('h3')

# Getting text and store in list
for name in hemispheres:
    hemi_names.append(name.text)
    
hemi_names   


# ### Getting full-sized hemisphere images

# In[29]:


# Search for thumbnail links
thumbnail_results = results[0].find_all('a')
thumbnail_links = []

for thumbnail in thumbnail_results:
    # If the thumbnail element has an image then 
    if (thumbnail.img):
        # then grab the attached link
        thumbnail_url = 'https://astrogeology.usgs.gov/' + thumbnail['href']
        
        # Append list with links
        thumbnail_links.append(thumbnail_url)

thumbnail_links


# In[32]:


#Extract full-size images
full_img = []
for url in thumbnail_links:
    
    # Visit every url
    browser.visit(url)
    html = browser.html
    new_soup = soup(html, 'html.parser')
    
    #Scrape each page for the image path
    results = new_soup.find_all('img', class_= 'wide-image')
    relative_img_path = results[0]['src']
    
    # Combine the reltaive image path to get the full url
    img_link = 'https://astrogeology.usgs.gov/' + relative_img_path

    # Add full image links to a list
    full_img.append(img_link)

full_img


# ### Store the results as a list of dictionaries 

# In[33]:


# Zip together the list of hemisphere names and hemisphere image links
mars_hemi_zip = zip(hemi_names, full_img)

hemisphere_image_urls = []

# Iterate through the zipped object

for tittle, img in mars_hemi_zip:
    
    mars_hemi_dict = {}
    
    #Adding titles to the dictionary
    mars_hemi_dict['tittle'] = tittle
    
    #Adding images to the dictionary
    mars_hemi_dict['img'] = img
    
    # Append the list with dictionaries
    hemisphere_image_urls.append(mars_hemi_dict)
    
hemisphere_image_urls


# In[ ]:


#leave the browser 
browser.quit()

