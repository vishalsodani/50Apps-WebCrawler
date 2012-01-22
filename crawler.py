from BeautifulSoup import BeautifulSoup
import sys
import requests
import traceback
import re

def crawl_url(url, searchtext, depth = 1):
    r = requests.get(url)
    urls_with_search_text = []
    soup = BeautifulSoup(r.content)
    links = soup.findAll(href=re.compile('^http'))
    for link in links:
        try:
            r = requests.get(link['href'])
            soup = BeautifulSoup(r.content)
            found = soup.findAll(text=re.compile('^SOPA'))
            if len(found) > 0:
                urls_with_search_text.append(link['href'])
        except:
            traceback.print_exc()
            print link

    print urls_with_search_text
        
    

if __name__ == '__main__':
    var = raw_input("Enter url to crawl: ")
    searchtext = raw_input("Enter seacrhtext: ")
    crawl_url(var,searchtext)

