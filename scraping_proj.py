from bs4 import BeautifulSoup
import selenium
#since using chrome
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import csv
import json
import requests
import time
from time import sleep, time


#url="https://www.amazon.com/s?k="


def get_url(url_search):
    temp = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss_1'
    url_search = url_search.replace(' ','+')

    url=temp.format(url_search)
    url+='&page={}'
    
    return url


def extract_record(prod):
    
    #Product name:
    
    '''finding element by xpath method didnt work with me
    prod_name ="Name: "+ prod.find_element_by_xpath('//*[@class="a-size-medium a-color-base a-text-normal"]')
    '''
    prod_name ="Name: "+ prod.h2.a.text.strip()

    #price
    try:
        price_parent = prod.find('span','a-price')
        price = "Price: "+price_parent.find('span','a-offscreen').text
    except AttributeError:
        return

    #extract url

    urls = 'https://www.amazon.com' + prod.h2.a.get('href')
   
    result = (prod_name,price,urls)
    return result

    


def main(url_search):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options, executable_path=r'C:\dev-projects\Scrape proj\chromedriver_win32_90\chromedriver.exe')
    driver.set_window_size(1800, 900)
    scrollScript="window.scrollTo({top:document.documentElement.scrollHeight, behavior: 'smooth'});"
    is_scroll= True

    records=[]
    url = get_url(url_search)
            
    for page in range(1,3):
        driver.get(url.format(page))

        if is_scroll:
            driver.execute_script(scrollScript) 
            driver.implicitly_wait(20)
            sleep(2)
        soup = BeautifulSoup(driver.page_source,'html.parser')
        result = soup.find_all('div',{'data-component-type':'s-search-result'})

        

        for prod in result:
            record = extract_record(prod)
            if record:
                records.append(record)
                
    '''I want to loop through every url scraped and find first product name but I have issue with writing the code correctly:

        for url in records:
            driver.get(url)
            
            #name
            name = driver.find_elements_by_xpath('//span[@id="productTitle"]')

        #for names in name:

        recordss=records + records.append(name)
    '''
        

        
    driver.close()

    with open('scrape.json', 'w') as f:

        json.dump(records,f,indent=2)

main('laptop screen')



