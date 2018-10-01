from bs4 import BeautifulSoup
import requests

def get_page_data():
    # Specify url to scrape from
    target_url = requests.get("https://davidachang.github.io/about/")
    page_data = BeautifulSoup(target_url.content, "html.parser")
    return page_data.body.contents

