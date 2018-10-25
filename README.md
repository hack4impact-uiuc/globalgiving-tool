# Global Giving Tool


# Command Line tool

## API

*gg list* => get all the scrapers availible


*gg log <scraper_name>* => lets you choose the timestamp => gets logs for how that information was scraped for that nonprofit


*gg run <scraper_name>* => kicks off a job to run that scraper and update the database


*gg submit* => from our database, take all new entries, format them, and send them to global givings central database


## Contributing Guidelines

Run ```pip install --editable .``` which will initialize your cli tool
Run ```gg -h``` to see the commands and run them

Deleting pyc files ```find . -name '*.pyc' -delete```

## API

# Microservices

Global Giving's focus of this project is to scrape as many directories of nonprofits. This helps them know who to reach out to and have as much information beforehand as possible. 

Every microservice is a scraper for a specific url that will give us as much information as possible. 


## Contributing Guidelines

### Adding a new microservice for scraping a new website

Step 1: Make a new folder with called "scraper-```<name of what your scraping>```

Step 2: Add a file called ```app.py``` and copy paste this boilerplate code in. This starts up a flask server and sets up a basic route. 

```Python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def my_first_route():
	return "Hello World!"

if __name__ == '__main__':
	app.run(debug=True)
```

Step 3: Run ```pip3 install pipreqs```

Step 4: Navigate to inside the folder, and run ``` pipreqs . ```. This should generate a ```requirements.txt``` file.

Step 6: Run ```pip3 install pipenv```

Step 7: Run ```pipenv shell```

Step 8: Run ```pip3 install -r requirements.txt``` to install everython from requirements.txt

Step 9: Run ```python3 app.py``` from command line, it will start up the server. 

If you navigate to ```http://127.0.0.1:5000/``` it will say Hello World. 

### Unit Testing
When new web scrapers or any new feature is added, unit testing must be done to ensure code functionality. All of the test files will be stored in the `tests` directory within your own microservice directory and will be run using the `pytest` python module. CircleCI will be running the test cases and they will be checked prior to merging.

In order for unittest to recognize and run tests, each method in the class should start with the pattern `test_`. The methods `setUp()` and `tearDown()` can also be used to set up the environment prior to testing. After all of the test cases have been written, they can all be run using `pytest`, which will find and run all tests that have the specified pattern in files in the current directory and any subdirectories.






