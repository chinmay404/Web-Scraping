from lib2to3.pgen2 import driver
import selenium
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from autoscraper import AutoScraper


to_serch = input("Enter Name : ")
driver = webdriver.Chrome(executable_path=r"C:\Users\Admin\Desktop\Project\Web Scrapping\Automated\chromedriver.exe")
url1 = "https://www.amazon.in/"
driver.get(url1) 
search =driver.find_element(By.ID, "twotabsearchtextbox")  
search.send_keys(to_serch)
search.send_keys(Keys.RETURN)
url = driver.current_url
# time.sleep(10)

# AUTO SCRAPER


# wanted_list = ["Apple iPhone 11 (64GB) - Black" ,"₹41,999 ",]
# scraper = AutoScraper()
# result = scraper.build(url, wanted_list)
# r1 = scraper.get_result_exact(url , grouped=True)
# print(r1)
# r2=scraper.set_rule_aliases({'rule_sfqk' : 'Name' , 'rule_la55' : 'price'})
# print(r2)


#Baeutiful soup
HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64)AppleWebKit/537.36 (KHTML, like Gecko)Chrome/44.0.2403.157 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'})
source = requests.get(url,headers=HEADERS)
soup = BeautifulSoup(source.text,'html.parser')

    
price = soup.find(class_="a-price-whole").get_text(strip=True)
name = soup.find(class_="a-size-medium a-color-base a-text-normal").get_text(strip=True)
print(name,price)





 