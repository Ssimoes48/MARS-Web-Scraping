from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

    #mars news
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    soup = bs(browser.html, 'html.parser')

    news_title = soup.find("div", class_="list_text").find("div", class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text
 
    #mars image
    mars_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(mars_url)

    browser.find_by_id("full_image").click()
    browser.find_by_text("more info     ").click()
    
    soup = bs(browser.html, 'html.parser')

    relative_image_path = soup.find("img", class_="main_image")["src"]

    mars_img = "https://www.jpl.nasa.gov/" + relative_image_path

    #mars facts
    facts_url = "https://space-facts.com/mars/"

    tables = pd.read_html(facts_url)

    facts_df = tables[0]
    facts_table = facts_df.to_html()

    #mars hem images
    hem_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hem_url)

    hem_img_urls = []

    for i in range(4): 
        browser.find_by_tag('h3')[i].click()
        soup = bs(browser.html, 'html.parser')
        img_title = soup.find("h2", class_="title").text
        img_url = soup.find("a", text ="Sample")["href"]
        hem_dic = {"title": img_title, "url": img_url}
        hem_img_urls.append(hem_dic)
        browser.back()

    #mars dictionary
    mars_dict = {"news_title": news_title, "news_p": news_p, "mars_img": mars_img, "facts_table": facts_table, "hem_img_urls": hem_img_urls}

    #quit browser
    browser.quit()

    return mars_dict


