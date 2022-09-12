from msilib.schema import Directory
from selenium import webdriver


dir = 'report'
Product_name = "IpAD" #input("Name : ")
min_price =  10000         #int(input("min : "))
max_price = 70000          #int(input("max : "))
Deafult_url = "https://www.amazon.in/"
filter_s = {
   'min' : min_price, 'max' : max_price
}
    


def web_driver(options):
    return  webdriver.Chrome(executable_path=r"C:\Users\Admin\Desktop\Project\Web Scrapping\Automated\chromedriver.exe",chrome_options=options)
    
def web_driver_options():
    return webdriver.ChromeOptions();

def stealth(options):
    return options.add_argument("headless")

def ingnor_sc_error(options):
    return options.add_argument("--ignore-certificate-errors")