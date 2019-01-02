# Global Giving Scraper and Crawler Tool



## Problem
Currently, GlobalGiving connects with organizations based in the US along with some nonprofits in other countries. However, the process of finding and applying to GlobalGiving remains significantly easier within the United States. In certain countries, factors including lack of internet connectivity and lack of access to documents required by GlobalGiving has led to slower onboarding and discovery of the organization. 

## Solution 

### Scraping directories of nonprofits

We identified 8 different directories of nonprofits, scraping each one and gathering as much information as possible from the website. We placed each scraper in its own microservice, creating a universal API to interact with all the nonprofits. 

Through the command line tool you can get a list of the registered scrapers, run the scrapers, and fetch the logs of the run.

### Crawling for potential sources 
 
We wanted to create a crawler in which you can search for potential directories of nonprofits so you know the one's to scrape. To rank the list of nonprofits, we are currently using heuristics such as the number of subpages, number of nonprofits that match ones we have already found, and finding repeated structures on the webpage. 

### Architecture

![GitHub Logo](/resources/architecture.png)

#### Scrapers
Every scraper is it's own serverless microservice. The initial idea was that we wanted every scraper to be indepedent and have a familiar API such that the cli tool could handle adding and running new scrapers or transformations (such as adding registration ids) to the data. 

To do this, every scraper has a route four ```/url``` that tells you what site is being scraped, a ```\test``` endpoint for an example of what the scraped data looks like, and a ```\run``` endpoint that actually scrapes the entire website, populates the database with the nonprofits, and sends the logs to s3. 

In concept this makes it cleaner, but we wanted to remove all the pains of deploying each flask microservices, so we adopted a tool called how that allow's use to make serverless lambda deployments. It treats every flask endpoint as a lambda function and deploys it. If you are in any of the microservices folders, you simply run ```now && now alias``` to update. This reads the ```now.json``` file that tells it how to build it and what the routes should be. This allows us not to have to worry about the configurations for deployment and allows it to automatically scale.

There was one last concern, which was for how long some of the scrapers take to run, since these deployments do timeout. To handle this, if the ```\data``` endpoint returns a number of pages, it hits every one of the pages ```\page\<number>```, scraping a portion of the website and adding to to the database. This pagination allows us to get the rest of the data even if one of the pages fails, allows us to have better logging, and splits up the logic effectively.

#### Crawler

The crawler can be accessed through the cli tool such that you can crawl based on a search term. By default this scrapes the first 3 links, but you can add an argument to scrape more sites. It gather's basic information from the site to give you an indicator if it is a potential directory for nonprofit organizations. It ranks currently on the number of subpages, the number of phone numbers and addresses, the number of "ngo" related words. This is information that is a lot quicker to gather and a decent indicator of websites should be scraped. 

In the microservices folder, there is the logic for the crawler. To improve this function, add a new function to ```rank.py``` and call in in ```crawl_functions.py```

# Setup

## Installation

```
cd globalgiving 
pip3 install -r requirements.txt
cd ..
pip3 install --editable .
globalgiving -h
```

## Command Line Tool

## Authentication

* **globalgiving register** 
Prompts you for your aws keys and mongo uri. It returns you a token with all the relevant information.

* **globalgiving login** 
Prompts you for your mongo uri and token, and fetches the rest of the information for you.

* **globalgiving logout** 
Logs you out and clears your information

* **globalgiving whoami** 
Tells you what your token and mongo uri currently are. 

## Registering and deleting scrapers

* **globalgiving add <scrape_name> <scrape_url>** 
Register that scraper url with a given name, or will update that scraper
    * Example: globalgiving add vietnam https://gg-scraper-viet.now.sh

* **globalgiving delete <scrape_name>** 
Removes that scraper from the list of scrapers in the database
    * Example: globalgiving delete vietnam 


## Getting metadata from scrapers 

* **globalgiving list** 
Lists all the scrapers availible

* **globalgiving urls**
Lists all of the base urls that the scrapers are gathering information from

* **globalgiving url <name>**
Get the url being scraped for that scraper

* **globalgiving test <scrape_name>** 
Uses the test endpoint to give you an example of what the data looks like
    * Example: globalgiving delete vietnam 



## Running scrapers 

* **globalgiving run <scrape_name> -a** 
Runs the scraper on the entire directory and adds all the nonprofits to the database. This command can be called without a scraper name and just with the -a flag, which signifies to run all of the available scrapers.
    * Example: globalgiving run australia

* **globalgiving log <scrape_name>** 
Gets a list of all uploaded logs from every run of the scraper
    * Example: globalgiving run australia

* **globalgiving log  <scraper_name> <file_name>** 
Downloads the log file locally for that scraper run
    * Example: globalgiving log australia 008deece-bcf7-4bff-90eb-9566e401e84e.txt


## Web Crawing

* **globalgiving crawl country=<country_name>**
This command will search for the specified country name using the Google Search API and rank each resulting link based
on the presence of certain characteristics, including the number of external links as well as the number of occurrences 
of NGO and directory.

* **globalgiving crawled**
Every time that the crawl command is utilized, the command line tool will store the links that it ranked as well as the resulting composite store in a database. Using the crawled command will retrieve the ranked pages and display them in descending order of rank.

## Adding a new microservice

* **globalgiving generate <scraper_name>** 
This will generate the scraper in the microservices folder with everything autogenerated. Then navigate to ```microservices/scraper-<scraper_name>/app/scraper.py``` and modify it to scrape the website you specified. 


## Handoff: Integrating it into globalgivings pipeline

* **globalgiving submit** 
This currently writes all the scraped ngos to ````~/globalgiving/ngo_data.json````, but in reality should be talking to globalgivings central database of nonprofits. 




