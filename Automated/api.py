import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Scraper(object):
    def __init__(self, *args):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)

    def get_page_source(self, url, filter_by):
        # dropdown = self.driver.find_element(By.ID, "s-result-sort-select")
        # self.driver.execute_script("arguments[0].click();", dropdown)
        sort_by_options = {
            'low-high': 'price-asc-rank',
            'high-low': 'price-desc-rank',
            'avg customer review': 'review-rank',
            'new arrival': 'date-desc-rank'
        }
        modified_url = url+'&'+sort_by_options.get(filter_by.lower())
        print(modified_url)
        self.driver.get(modified_url)
        # sort_by_value = sort_by_options.get(filter_by.lower())
        # if sort_by_value:
        #     sortby = self.driver.find_element(
        #         By.CSS_SELECTOR, f"option[value='{sort_by_value}']")
        #     sortby.click()
        page_source = self.driver.page_source
        if page_source is not None:
            return page_source
        else:
            print("Page Data : none")

    def scrape_amazon(self, search_query, filter_by='rating', top=10):
        url = f"https://www.amazon.in/s?k={search_query}"
        page_source = self.get_page_source(url, filter_by)
        soup = BeautifulSoup(page_source, 'html.parser')
        search_results = soup.select(
            "div[data-component-type='s-search-result']")
        scraped_data = []
        counter = 0

        for result in search_results:
            if counter >= top:
                break

            product_title = result.select_one("h2 a span").text.strip()
            product_price = result.select_one(
                ".a-price span span").text.strip()
            product_link = result.select_one("h2 a").get('href')
            product_image = result.select_one(".s-image").get('src')
            product_rating = result.select_one("span.a-icon-alt").text.strip()

            item = {
                'Title': product_title,
                'Price': product_price,
                'Link': f"https://www.amazon.in{product_link}",
                'Image': product_image,
                'Rating': product_rating
            }
            scraped_data.append(item)
            counter += 1
            self.write_to_file(item, search_query, 'amazon')
        return scraped_data

    def scrape_flipkart(self, search_query, filter_by='rating', top=50):
        url = f"https://www.flipkart.com/search?q={search_query}"
        page_source = self.get_page_source(url, filter_by)
        soup = BeautifulSoup(page_source, 'html.parser')
        search_results = soup.select("div[data-id]")
        scraped_data = []
        counter = 0

        for result in search_results:
            if counter >= top:
                break

            product_title = result.select_one(
                "a[data-id] > div > div > div > a").text.strip()
            product_price = result.select_one(
                "div ._30jeq3._1_WHN1").text.strip()
            product_link = result.select_one("a[data-id]").get('href')
            product_image = result.select_one("a[data-id] img").get('src')
            product_rating = result.select_one("div._3LWZlK").text.strip()
            item = {
                'Title': product_title,
                'Price': product_price,
                'Link': f"https://www.flipkart.com{product_link}",
                'Image': product_image,
                'Rating': product_rating
            }
            scraped_data.append(item)
            counter += 1
        return scraped_data

    def close(self):
        self.driver.quit()

    def write_to_file(self, item, search_query, by):
        with open(by+'_'+search_query+'.json', 'a') as file:
            json.dump(item, file)
            file.write('\n')


class ScraperApp(object):
    def __init__(self):
        self.scraper = Scraper()

    def run(self, search_query, duration_minutes, filter_by='rating', top=50):
        self.scrape_and_notify(search_query, filter_by, top)
        duration_seconds = duration_minutes * 60

        while True:
            time.sleep(duration_seconds)
            self.scrape_and_notify(search_query, filter_by, top)

    def scrape_and_notify(self, search_query, filter_by, top):
        amazon_data = self.scraper.scrape_amazon(search_query, filter_by, top)
        # flipkart_data = self.scraper.scrape_flipkart(
        #     search_query, filter_by, top)
        self.send_notification(amazon_data, "Amazon")
        # self.send_notification(flipkart_data, "Flipkart")

    def send_notification(self, data, platform):
        # Implement your notification logic here
        # This could include sending an email, SMS, or any other notification method
        # You can access the scraped data (JSON format) and the platform name (e.g., "Amazon" or "Flipkart")

        # Example: Send an email with the scraped data
        subject = f"Scraped Data from {platform}"
        message = json.dumps(data, indent=4)
        send_email(subject, message)


def send_email(subject, message):
    # Implement your email sending logic here
    # This could use a library like smtplib to send the email
    pass


if __name__ == '__main__':
    search_query = input("Enter the search query: ")
    duration_minutes = int(input("Enter the duration in minutes: "))
    filter_by = input(
        "Sort By: \n1.Low-High\n2.High-Low\n3.Avg Customer Review\n4.New Arrival\nEnter the option number: ")
    filter_options = {
        '1': 'low-high',
        '2': 'high-low',
        '3': 'avg customer review',
        '4': 'new arrival'
    }
    filter_by_value = filter_options.get(filter_by)
    if not filter_by_value:
        print("Invalid option number.")
        exit()
    top = int(input('Top: '))
    app = ScraperApp()
    app.run(search_query, duration_minutes, filter_by_value, top)
