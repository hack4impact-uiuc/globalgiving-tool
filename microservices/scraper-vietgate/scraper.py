from bs4 import BeautifulSoup
from requests import get
from org import create_org

url = 'https://www.viet.net/community/nonprofit/'

def get_page_data():
    response = get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    for link in soup.findAll('p'):
        parse_data(link.text)

def parse_data(link):
    if link == None:
        return
    for line in link.split('\n\n'):
        create_org(line.strip().split('\n'))

if __name__ == '__main__':
    get_page_data()