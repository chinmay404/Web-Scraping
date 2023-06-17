import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


class Scraper(object):
    def __init__(self, *args):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)

    def get_page_source(self, url):
        self.driver.get(url)
        return self.driver.page_source

    def scrape_amazon(self, search_query):
        url = f"https://www.amazon.in/s?k={search_query}"
        page_source = self.get_page_source(url)
        soup = BeautifulSoup(page_source, 'html.parser')
        search_results = soup.select(
            "div[data-component-type='s-search-result']")
        scraped_data = []

        for result in search_results:
            product_title = result.select_one("h2 a span")
            product_price = result.select_one(".a-price span span")
            product_link = result.select_one("h2 a")
            product_image = result.select_one(".s-image")

            if product_title and product_price and product_link and product_image:
                item = {
                    'Title': product_title.text.strip(),
                    'Price': product_price.text.strip(),
                    'Link': f"https://www.amazon.in{product_link.get('href')}",
                    'Image': product_image.get('src')
                }

                scraped_data.append(item)

        return scraped_data

    def scrape_flipkart(self, search_query):
        url = f"https://www.flipkart.com/search?q={search_query}"
        page_source = self.get_page_source(url)
        soup = BeautifulSoup(page_source, 'html.parser')
        search_results = soup.select("div[data-id]")
        scraped_data = []

        for result in search_results:
            product_title = result.select_one("a[data-id] > div")
            product_price = result.select_one("div ._30jeq3._1_WHN1")
            product_link = result.select_one("a[data-id]")
            product_image = result.select_one("a[data-id] img")

            if product_title and product_price and product_link and product_image:
                item = {
                    'Title': product_title.text.strip(),
                    'Price': product_price.text.strip(),
                    'Link': f"https://www.flipkart.com{product_link.get('href')}",
                    'Image': product_image.get('src')
                }

                scraped_data.append(item)

        return scraped_data

    def close(self):
        self.driver.quit()


class ScraperApp(object):
    def __init__(self):
        self.scraper = Scraper()

    def run(self, search_query, duration_minutes):
        self.scrape_and_notify(search_query)
        duration_seconds = duration_minutes * 60
        while True:
            time.sleep(duration_seconds)
            self.scrape_and_notify(search_query)

    def scrape_and_notify(self, search_query):
        amazon_data = self.scraper.scrape_amazon(search_query)
        flipkart_data = self.scraper.scrape_flipkart(search_query)
        self.send_notification(amazon_data, "Amazon")
        self.send_notification(flipkart_data, "Flipkart")

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

    app = ScraperApp()
    app.run(search_query, duration_minutes)
