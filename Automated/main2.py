from itertools import product
from time import sleep
from unicodedata import name
from config import (Deafult_url,Product_name,web_driver_options,web_driver,stealth,ingnor_sc_error,filter_s)
import config 
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys


class report:
     def __init__(self):
            pass
  
    
class API:
    def __init__(self, Product_name , filters ,Deafult_url):
        self.url = Deafult_url
        self.to_search = Product_name
        options = web_driver_options()
        stealth(options)
        ingnor_sc_error(options)
        self.Driver = web_driver(options)
        self.filter_P = f"&rh=p_36%3A{filter_s['min']}00-{filter_s['max']}00"
        pass
    
    
    def run(self):
        print("currently : Executing .... ")
        print("currently : Searching : ", self.to_search)
        anchor = self.get_links()
        product = self.get_info(anchor)
        # self.Driver.close()
    

    def get_info(self, anchor):
        print("Get_Info Working")
        clear_url = self.get_clear_url(anchor)
        print(clear_url)
        products = [] 
        for one in clear_url:
            products = self.get_single(one)
            
    def get_clear_url(self, anchor):
        return [self.get_asin(anchor) for link in anchor]
    
    def get_asin(product_link):
        return product_link[product_link.find('/dp/') + 4:product_link.find('/ref')]
    
    def get_single(self,one) : 
        print("ID : {one}") 
        short = self.url+'dp/'+one
        self.Driver.get(f'{short}')      
        sleep(10)
        title= self.Driver.find_element(By.ID,'productTitle').text
        price =  '1000'
        print(title,price)
        
        
       
    def get_links(self):
        print("get_links  Running")
        self.Driver.get(self.url)
        search =self.Driver.find_element (By.ID, "twotabsearchtextbox") 
        search.send_keys(self.to_search)
        search.send_keys(Keys.RETURN)
        self.Driver.get(f'{self.Driver.current_url}{self.filter_P}')
        print("1")
        result_list = self.Driver.find_elements(By.CLASS_NAME,'s-result-list')
        print(result_list)
        links = []
        try:
            results = result_list[0].find_elements(By.XPATH,
                "//div/span/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/h2/a")
            links = [link.get_attribute('href') for link in results]
            print(results)
            return links
        
        except Exception as e:
            print("No Matching Found ...")
            print(e)
            return links



 
if __name__=='__main__':

    key = API(Product_name,filter,Deafult_url)
    # print(key.filter_P)
    # print(key.to_search)
    key.run()
    
    