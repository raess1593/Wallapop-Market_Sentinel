from scraper import WallapopScraper
from processor import DataProcessor
import argparse

if __name__ == "__main__":
    # Receive and parse arguments
    parser = argparse.ArgumentParser(description="Wallapop Market Sentinel Scraper")
    parser.add_argument("--search", type=str, default="nike", help="Key word to search ex: nike")
    parser.add_argument("--limit", type=int, default=10, help="Number of articles to extract ex: 200")

    args = parser.parse_args()
    scraper = WallapopScraper()

    # Search a specific url according to the parameters
    base_url = "https://es.wallapop.com/search?keywords="
    params = "&order_by=most_relevance"
    search_query = args.search.replace(" ", "%20")
    url = f"{base_url}{search_query}{params}"
    scraper.fetch_page(url)
    
    # Get data
    scraper.get_page_articles(args.limit)
    raw_data = scraper.data

    # Convert data to a clean dataframe
    df_object = DataProcessor(raw_data)
    df = df_object.clean()
    print(df)

    scraper.close()