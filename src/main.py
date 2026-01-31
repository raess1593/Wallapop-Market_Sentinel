from scraper import WallapopScraper

if __name__ == "__main__":
    scraper = WallapopScraper()

    url1 = "https://es.wallapop.com/search?keywords="
    url2 = "&order_by=most_relevance"
    input_url = "nike"

    scraper.fetch_page(url1+input_url+url2)
    
    scraper.get_page_articles()
    scraper.close()