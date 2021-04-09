# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 16:08:39 2020

@author: zemone
"""
import urllib.request
from bs4 import BeautifulSoup
import time
from decantaloCrawler import DC
DCcrawler = DC()
urls = []
urls_champ = []

def save_data(data,path):
	import pickle
	fw = open(path,'wb')
	pickle.dump(data,fw)
	fw.close()

def load_data(path):
	import pickle
	fd = open(path,'rb')
	data = pickle.load(fd)
	fd.close()
	return data

#HtmlPage Read Func
def htmlPageRead(url,parse_option):
    try:
        headers = { 'User-Agent' : 'Mozilla/5.0' }
        request = urllib.request.Request(url, None, headers)
        conn = urllib.request.urlopen(request)
        status = conn.getcode()
        contentType = conn.info().get_content_type()
        if(status != 200 or contentType == "audio/mpeg"):
		    			raise ValueError('Bad Url...')
        html = conn.read().decode('utf-8')
        return BeautifulSoup(html, parse_option)
    except Exception as e:
        print (e)
def urlCatcher(baseurl,page,depth):
    print(str(depth) + " <-- current depth(" + baseurl + ")")
    urls = []
    if depth > 12:
        return urls
    soup = htmlPageRead(baseurl+page,'html5lib')
    #link de decanto
    #containers = soup.body.find_all("h3",class_="product-name-container")
    #link de infovines
    containers = soup.body.find_all("a", class_="joodb_titlelink")
    # Pot ser que estem en la ultima pag pero no hi ha items
    if len(containers) < 1:
        return urls
    for container in containers:
        #link de decanto
        #urls.append(container.a.get("href").strip())
        #link de infovines
        urls.append(baseurl + container.get("href").strip())
    # primer mirem si tenim boto de seguent (estem) en la ultima pag, aixo no funciona en algunes altres pagines
    #link de decanto
    #nextpage = soup.body.find("li",class_="pagination_next")
    nextpage = soup.body.find("li",class_="pagination-next")
    if (nextpage is None) or (nextpage.a is None):
        return urls
    # Despres agafem la url pertinent
    nextpage = nextpage.a.get("href")
    # Fem un sleep de 1 s per a complir amb crawl-delay: 1 del robots.txt
    time.sleep(1)
    urls.extend(urlCatcher(baseurl,nextpage,depth+1))
    return urls

def main(urls):
    print(len(urls))
    for index,url in enumerate(urls):
        #if index > 30:
         #   break
        soup = htmlPageRead(url,'html5lib')
        try:
            print(index)
            #DCcrawler.feedSoup(soup)
        except Exception as e:
            print(e)
            print('url : {} \nIteration : {}'.format(url,index))
        # Fem un sleep de 1 s per a complir amb crawl-delay: 1 del robots.txt
        time.sleep(1)
    #DCcrawler.writeLists()

if __name__ == "__main__":
    # catalunya
	# main("https://docat.cat/es/els-cellers/")
    # madrid
    """
    base_url = 'https://www.decantalo.com/en/buscar?controller=search&orderby=id_product&orderway=desc&search_query='
    url = base_url + url.replace(' ','+') + '&submit_search=Search'
    soup = htmlPageRead(url,'html5lib')
    # extreiem la url del primer producte resultant
    soup.body.find("a",class_="product-name").get('href')
    """
    urls = [];
    urls_champ = [];
    #urls = urlCatcher("https://www.decantalo.com","/es/vino/",0)
    urls = urlCatcher("https://www.infovinos.es","/bodegas?start=0",0)
    #urls = urlCatcher("https://www.decantalo.com","/es/vino/",0)
    #urls_champ = urlCatcher("https://www.decantalo.com","/es/espumosos/",0)
    #urls.extend(urls_champ)
    #no hay urls, hay que mirar porque
    main(urls)