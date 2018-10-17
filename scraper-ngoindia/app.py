from flask import Flask
from scraper import get_page_data
from scraper import get_ngo_data
from scraper import get_ngo_page_fromngos
from scraper import get_ngo_page_fromcounty
from scraper import compile_information

app = Flask(__name__)

@app.route('/')
def my_first_route():
	return "<h1> Hello World! </h1>"

@app.route('/data')
def page_data():
	return str(get_page_data())

if __name__ == '__main__':
	app.run(debug=True)
