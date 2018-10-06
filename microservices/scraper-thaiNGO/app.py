from flask import Flask
from scraper import basepage_scrape


from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/')
def my_first_route():
    basepage_scrape()
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True)