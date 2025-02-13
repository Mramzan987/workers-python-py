from utils.helpers.index import url_insert_bulk, get_sitemap_urls
from utils.slack import detailed_error_slack_message

COMPETITOR = "baypower"
URL = "https://www.baypower.com/pub/media/sitemap.xml"


def get_and_store_baypower_urls():
    try:
        outputs = []
        sitemap_urls = get_sitemap_urls(URL, COMPETITOR)
        print(f"Total URLs: {len(sitemap_urls)}")
        for data in sitemap_urls:
            result = {
                "competitor": COMPETITOR,
                "url": data,
                "scraper_type": "sitemap",
            }
            outputs.append(result)
            if len(outputs) == 5000:
                url_insert_bulk(outputs)
                outputs = []
        if outputs and len(outputs):
            url_insert_bulk(outputs)
    except Exception as e:
        detailed_error_slack_message(e, COMPETITOR)
