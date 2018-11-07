#AIzaSyB3wFpS5E0-p0YGEh2l2dW6xCz4ax5MwK0
#from google import google
from googlesearch import search

for url in search('ngo directory global', lang='es', num=10, pause=2.0, stop=20):
    print(url)
