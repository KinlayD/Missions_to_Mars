from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)    

    # Latest Mars News
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    time.sleep(1)

    for x in range(1):
        html = browser.html
        soup = bs(html, 'html.parser')
        image_and_descriptions = soup.find_all('section', class_='image_and_description_container')
        for text in image_and_descriptions:
            content_title_tag = text.find(class_="content_title").text
            news_title = content_title_tag
            news_p = text.find(class_="article_teaser_body").text
    

    # Featured Mars Image
    url_1 = 'https://spaceimages-mars.com/'
    browser.visit(url_1)
    time.sleep(1)

    for x in range(1):
        html_1 = browser.html
        soup_1 = bs(html_1, 'html.parser')
        header_html = soup_1.find_all('a', class_="showimg fancybox-thumbs")
        for link in header_html:
            img_tag = link['href']
            featured_image_url = url_1 + img_tag

    # Mars Facts
    url_3 = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url_3)
    mars_facts = tables[0]
    mars_facts.columns = mars_facts.iloc[0]
    mars_facts_df = mars_facts.iloc[1:].set_index('Mars - Earth Comparison')
    mars_facts_table_df = mars_facts_df.replace('\n', '')
    mars_facts = mars_facts_table_df.to_html()


    # Mars Hemispheres
    url_2 = 'https://marshemispheres.com/'
    browser.visit(url_2)
    time.sleep(1)
    html_2 = browser.html
    soup_2 = bs(html_2, 'html.parser')
        
    title =[]
    image_url = []
    hemisphere_image_urls = []
    item_html = soup_2.find_all('div', class_='item')
    for h3 in item_html:
        tag_text = h3.find('h3').text
        title.append(tag_text)
        time.sleep(1)

    for t in title:
        browser.links.find_by_partial_text(t).first.click()
        html_3 = browser.html
        soup_3 = bs(html_3, 'html.parser')
        sample_img = soup_3.find_all('a', string='Sample')
        for img in sample_img:
            time.sleep(1)
            image_url.append(img['href'])
            browser.find_by_tag('h3').last.click()

    full_image_url = [url_2 + url for url in image_url]
    title_and_url = zip(title, full_image_url)

    for t, u in title_and_url:
        title_and_url_dict = {'title': t,'img_url': u}
        hemisphere_image_urls.append(title_and_url_dict)

    
    browser.quit()
    mars_dict = {'news_title': news_title, 'paragraph_text': news_p, 'featured_image_url': featured_image_url, 
    'mars_facts': mars_facts, 'hemisphere_image_urls': hemisphere_image_urls}
    return mars_dict


