from flask import Flask
from flask_restplus import Resource, Api, fields
from werkzeug.contrib.fixers import ProxyFix
from src.scraper import scrape, scrape_page, srape_page_urls

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app)


@api.route("/url")
class Scraper(Resource):
    def get(self):
        return "http://www.hati.my/"


@api.route("/data")
class Scraper(Resource):
    def get(self):
        orgs = scrape()
        return {"pages": orgs["pages"]}


@api.route("/page/<number>")
class Scraper(Resource):
    def get(self, number):
        links = srape_page_urls(int(number))
        orgs = scrape_page(links["urls"][0])
        return {"data": orgs}


@api.route("/test")
class ScraperVietnam(Resource):
    def get(self):
        org = scrape(one=True)
        return {"test": org[0]}


if __name__ == "__main__":
    app.run(debug=True)
