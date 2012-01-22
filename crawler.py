from BeautifulSoup import BeautifulSoup
import sys
import requests

def crawl_url(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    links = soup.findAll('a')
    for link in links:
        print link['href']
    

if __name__ == '__main__':
    var = raw_input("Enter url to crawl: ")
    crawl_url(var)

