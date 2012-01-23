from BeautifulSoup import BeautifulSoup
import requests
import traceback
import re
from sets import Set

URL_TO_CRAWL = ""
SEARCH_TEXT = ""


def crawl_url():
    #if not 'http' in URL_TO_CRAWL:
        #URL_TO_CRAWL = 'http://' + URL_TO_CRAWL 
    web_page = requests.get(URL_TO_CRAWL)
    urls_with_search_text = []
    webpage_content = BeautifulSoup(web_page.content)
    links = webpage_content.findAll('a',attrs={"href":re.compile('^http')})
    
    urls_with_search_text = process_links(links, 1)
    print urls_with_search_text


def process_links(links, depth):
    urls_with_search_text = Set()

    if depth > 3:
        return urls_with_search_text

    for link in links:
        try:
            web_page = requests.get(link['href'], timeout = 3,allow_redirects=False)
            print "processing %s..." % (link['href'])

            webpage_content = BeautifulSoup(web_page.content)
            found = webpage_content.findAll(text=re.compile('^' + SEARCH_TEXT))

            if len(found) > 0:
                urls_with_search_text.add(link['href'])


            links_new = webpage_content.findAll('a',attrs={"href":re.compile('^http')})

            for res in process_links(links_new, depth + 1):
                urls_with_search_text.add(res)
            
        except requests.ConnectionError:
            traceback.print_exc()
            print link
        except requests.URLRequired:
            print "invalid url %s" % (link)
        except ValueError:
            traceback.print_exc()
        except requests.RequestException:
            traceback.print_exc()
        

    return urls_with_search_text
    

if __name__ == '__main__':
    URL_TO_CRAWL = raw_input("Enter url to crawl: ")
    SEARCH_TEXT = raw_input("Enter searchtext: ")
    crawl_url()

