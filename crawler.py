from BeautifulSoup import BeautifulSoup
import requests
import traceback
import re

URL_TO_CRAWL = ""
SEARCH_TEXT = ""


def crawl_url():
    web_page = requests.get(URL_TO_CRAWL)
    urls_with_search_text = []
    soup = BeautifulSoup(web_page.content)
    links = soup.findAll(href=re.compile('^http'))
    
    urls_with_search_text = process_links(links, 1)
    print urls_with_search_text


def process_links(links, depth):
    urls_with_search_text = []
    if depth > 3:
        return urls_with_search_text
    for link in links:
        try:
            web_page = requests.get(link['href'])
            soup = BeautifulSoup(web_page.content)
            found = soup.findAll(text=re.compile('^' + SEARCH_TEXT))
            if len(found) > 0:
                urls_with_search_text.append(link['href'])
            links_new = soup.findAll(href=re.compile('^http'))
            for res in process_links(links_new, depth + 1):
                urls_with_search_text.append(res)
            
        except:
            traceback.print_exc()
            print link

    return urls_with_search_text
    

if __name__ == '__main__':
    URL_TO_CRAWL = raw_input("Enter url to crawl: ")
    SEARCH_TEXT = raw_input("Enter searchtext: ")
    crawl_url()

