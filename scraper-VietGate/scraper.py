from bs4 import BeautifulSoup
from requests import get

url = 'https://www.viet.net/community/nonprofit/'

def get_page_data():
    response = get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(len(soup.findAll('p')))
    for link in soup.findAll('p'):
        parse_data(link.text)

def parse_data(link):
    if link == None:
        return
    for line in link.split('\n\n'):
        if len(line) > 0:
            print(list(filter(None, line.splitlines())))

if __name__ == '__main__':
    get_page_data()