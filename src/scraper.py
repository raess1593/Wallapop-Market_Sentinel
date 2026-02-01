import undetected_chromedriver as uc
uc.Chrome.__del__ = lambda self: None

from webdriver_manager.core.os_manager import OperationSystemManager, ChromeType

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from bs4 import BeautifulSoup as bs

import time
import random

class WallapopScraper:
    def __init__(self):
        # Configure undetected options
        self.options = uc.ChromeOptions()
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        ]
        self.options.add_argument(f"--user-agent={random.choice(user_agents)}")
        self.options.add_argument('--disable-features=Translate')
        self.options.add_argument('--lang=es-ES')
        self.options.add_argument('--headless=new')

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
    def get_page_articles(self, n):
        try:
            self.load_more()
        except:
            pass

        # Load n products
        products_loaded = []
        scroll_counter = 0
        pixels = random.uniform(2000, 4000)

        while len(products_loaded) < n:
            current_count = len(products_loaded)
            self.driver.execute_script(f"window.scrollBy(0, {pixels});")
            time.sleep(random.uniform(2, 4))

            products_loaded = self.driver.find_elements(By.CSS_SELECTOR, "div[class*='ItemCard__content']")
            
            # Break loop if no more articles are detected
            if len(products_loaded) == current_count:
                scroll_counter += 1
            else:
                scroll_counter = 0
            if scroll_counter > 3:
                break
        
        self.save_to_data(products_loaded[:n])

    # Click "Load more" button
    def load_more(self):
        host_selector = self.wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "div[class*='loadMore']")))

        shadow_host = host_selector.find_element(By.CSS_SELECTOR, "walla-button")

        shadow_root = shadow_host.shadow_root
        button = shadow_root.find_element(By.CSS_SELECTOR, "button")
        
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
        time.sleep(random.uniform(1, 2))
        self.driver.execute_script("arguments[0].click();", button)
        
    # Save in self.data all the loaded products
    def save_to_data(self, products):
        for p in products:
            product_name = p.find_element(By.CSS_SELECTOR, "h3[class*='ItemCard__title']").text
            price =  p.find_element(By.CSS_SELECTOR, "[aria-label='Item price']").text
            self.data.append({
                "product_name": product_name,
                "price": price,
                "shipping_available": self.check_exists(p, "wallapop-badge[badge-type*='shippingAvailable']"),
                "outstanding": self.check_exists(p, "p[class*='bump-label']")
            })

    # Ignore error if not found
    def check_exists(self, parent, element):
        try:
            parent.find_element(By.CSS_SELECTOR, element)
            return True
        except:
            return False

    # Close page
    def close(self):
        if self.driver:
            try:
                self.driver.quit()
            except:
                # Ignore error closing
                pass