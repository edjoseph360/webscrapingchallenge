from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests

executable_path = {"executable_path": "./chromedriver.exe"}
browser = Browser("chrome", **executable_path)

def scrapeeverything():
    final_data = {}
    output = marsNews()
    final_data["mars_news"] = output[0]
    final_data["mars_paragraph"] = output[1]
    final_data["mars_image"] = marsImage()
    final_data["mars_weather"] = marsWeather()
    final_data["mars_facts"] = marsFacts()
    final_data["mars_hemisphere"] = marsHem()

    return final_data

def marsNews():
    print(browser)

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")
    slide_element = news_soup.select_one("ul.item_list li.slide")
    news_title = slide_element.find("div", class_="content_title").get_text()
    news_paragraph = slide_element.find("div", class_="article_teaser_body").get_text()
    output = [news_title, news_paragraph]
    return output

def marsImage():
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    image = soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + image
    return featured_image_url

def marsWeather():
    url_weather = 'https://twitter.com/marswxreport?lang=en'
    res_weather = requests.get(url_weather)
    weather_soup = BeautifulSoup(res_weather.text, 'lxml')
    weather_mars = weather_soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text.strip()
    return weather_mars

def marsFacts():
    facts = pd.read_html("https://space-facts.com/mars/")[0]
    facttable = pd.DataFrame(facts)
    facttable.columns=["Description", "Value"]
    mars_facts = facttable.to_html(index = True, header =True)
    return mars_facts

def marsHem():
    title = hemisphere.find("h3").text
    end_link = hemisphere.find("a")["href"]
    image_link = "https://astrogeology.usgs.gov/" + end_link    
    browser.visit(image_link)
    html = browser.html
    soup=BeautifulSoup(html, "html.parser")
    downloads = soup.find("div", class_="downloads")
    image_url = downloads.find("a")["href"]
    mars_hemisphere.append({"title": title, "img_url": image_url})
    return mars_hemisphere

