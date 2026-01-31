import undetected_chromedriver as uc
uc.Chrome.__del__ = lambda self: None

from webdriver_manager.core.os_manager import OperationSystemManager, ChromeType

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from bs4 import BeautifulSoup as bs

import time
import random

import pandas as pd

class WallapopScraper:
    def __init__(self):
        # Configure undetected options
        self.options = uc.ChromeOptions()
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        ]
        self.options.add_argument(f"--user-agent={random.choice(user_agents)}")
        
        # Initialize driver
        version = OperationSystemManager().get_browser_version_from_os(ChromeType.GOOGLE)
        self.main_version = int(version.split('.')[0])
        self.driver = uc.Chrome(options=self.options, version_main=self.main_version)
        self.wait = WebDriverWait(self.driver, 12)

        # Data
        self.data = []

    # Navigate to the page
    def fetch_page(self, url):
        # Ensure page loaded correctly
        try:
            self.driver.get(url)
            self.wait.until(ec.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(random.uniform(2, 4))
        
        except Exception as e:
            print(f"Error loading page: {e}")
    
    # Find and save products main info
    def get_page_articles(self):
        self.load_more()

        product_grid = self.driver.find_elements(By.CSS_SELECTOR, "div[class*='ItemCard__content']")
        
        for p in product_grid:
            product_name = p.find_element(By.CSS_SELECTOR, "h3[class*='ItemCard__title']").text
            price =  p.find_element(By.CSS_SELECTOR, "[aria-label='Item price']").text
            self.data.append({
                "product_name": product_name,
                "price": price
            })

    # Click "Load more" button
    def load_more(self):
        try:
            next_button = self.wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "span[part='button-next']")))
            next_button.click()
        except:
            return

    # Close page
    def close(self):
        if self.driver:
            try:
                self.driver.quit()
            except:
                # Ignore error closing
                pass