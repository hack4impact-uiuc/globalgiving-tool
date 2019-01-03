from flask import Flask, request, jsonify
from flask_restplus import Resource, Api, fields
from werkzeug.contrib.fixers import ProxyFix
from src.scraper import get_one_nonprofit, get_page_data, get_ngo_data
import json

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app)


@api.route("/url")
class Scraper(Resource):
    def get(self):
        return "https://ngosindia.com/ngos-of-india/"


@api.route("/data")
class Scraper(Resource):
    def get(self):
        return {"data": get_page_data()}


@api.route("/page", methods=["POST"])
class Scraper(Resource):
    def post(self):
        print((json.loads(request.json))["url"])
        org = get_ngo_data((json.loads(request.json))["url"])
        # print(org)
        return {"data": org}


@api.route("/test")
class Scraper(Resource):
    def get(self):
        return {"test": get_one_nonprofit()}


if __name__ == "__main__":
    app.run(debug=True)
