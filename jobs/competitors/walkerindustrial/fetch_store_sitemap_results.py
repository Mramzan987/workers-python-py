from utils.helpers.index import (
    url_insert_bulk,
    preprocess_manufacturers,
    get_sitemap_urls,
)
from utils.slack import detailed_error_slack_message

from .helper import (
    COMPETITOR,
    STARTING_URL,
    is_valid_url_and_manufacturer,
    is_manufacturer_match,
    MAX_COUNT,
)


def get_and_store_walker_industrial_urls():
    try:
        manufacturers_dict = preprocess_manufacturers()

        count = 0
        outputs = []

        sitemap_urls = get_sitemap_urls(STARTING_URL, COMPETITOR)
        print(f"Found {len(sitemap_urls)} sitemap urls")

        for sitemap_url in sitemap_urls:
            website_urls = get_sitemap_urls(sitemap_url, COMPETITOR)
            print(f"Found {len(website_urls)} website urls")

            for url in website_urls:
                is_valid, manufacturer = is_valid_url_and_manufacturer(url)

                if (
                    is_valid
                    and manufacturer
                    and is_manufacturer_match(manufacturers_dict, manufacturer)
                ):
                    count += 1
                    result = {
                        "competitor": COMPETITOR,
                        "url": url,
                        "scraper_type": "sitemap",
                        "from_manufacturer": True,
                    }
                    outputs.append(result)

                if count >= MAX_COUNT:
                    url_insert_bulk(outputs)
                    count = 0
                    outputs = []

        if outputs and len(outputs):
            url_insert_bulk(outputs)
            outputs = []

    except Exception as e:
        detailed_error_slack_message(e, COMPETITOR)
