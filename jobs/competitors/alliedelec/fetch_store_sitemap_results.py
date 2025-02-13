from .helper import store_data
from utils.helpers.index import (
    get_sitemap_urls,
    download_gz_file,
)
from utils.slack import detailed_error_slack_message
from config.index import API_KEY_SCRAPY


COMPETITOR = "alliedelec"
URL = "https://us.rs-online.com/sitemap.xml"


def get_and_store_alliedelec_urls():
    try:
        scrape_api = f"https://api.scraperapi.com/?api_key={API_KEY_SCRAPY}&url={URL}&render=true"
        sitemap_urls = get_sitemap_urls(scrape_api, COMPETITOR)
        print(f"Total URLs: {len(sitemap_urls)}")
        for count, data in enumerate(sitemap_urls, start=1):
            path = download_gz_file(COMPETITOR, data, count)
            store_data(path)
    except Exception as e:
        detailed_error_slack_message(e, COMPETITOR)
