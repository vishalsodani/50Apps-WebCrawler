from BeautifulSoup import BeautifulSoup
import requests
import traceback
import re

def crawl_url(url, searchtext):
    web_page = requests.get(url)
    urls_with_search_text = []
    soup = BeautifulSoup(web_page.content)
    links = soup.findAll(href=re.compile('^http'))
    
    urls_with_search_text = process_links(links, 1)
    print urls_with_search_text


def process_links(links, depth):
    urls_with_search_text = []
    if depth > 3:
        return urls_with_search_text
    counter = 0
    for link in links:
        if counter > 10:
            break
        counter = counter + 1    
        try:
            web_page = requests.get(link['href'])
            soup = BeautifulSoup(web_page.content)
            found = soup.findAll(text=re.compile('^' + searchtext))
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
    url = raw_input("Enter url to crawl: ")
    searchtext = raw_input("Enter seacrhtext: ")
    crawl_url(url, searchtext)

