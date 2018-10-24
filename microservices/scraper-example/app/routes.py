from app import app
from app.scraper import get_page_data

@app.route('/')
def index():
    return "Hello, Python World!"

@app.route("/data")
def page_data():
    return str(get_page_data())