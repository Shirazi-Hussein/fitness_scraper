# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 22:19:00 2020

@author: truet
"""
import contextlib
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

import bs4
import requests

def get_soup(url):
    """get soup of url"""
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.content, 'lxml')
    return soup

def get_availability_plates(url):
    """get availability of each plate item"""
    soup = get_soup(url)
    results = []
    #container for plates 
    container = soup.find('div', {'class':'container product-detail product-wrapper'})
    with contextlib.suppress(AttributeError):
        title = container.find('span', {'class':'h1 product-name'}).text.strip()
        price = container.find('span', {'class':'sales'}).text.strip()
        stock = container.find('span', {'class':'availability-msg'}).span.text.strip()
        title, price, stock = title, price, stock
        results.append(dict(title = title, price = price, stock = stock, url = url))
    return results
    

def main():
    url = "https://www.titan.fitness/strength/weight-plates/"
    soup = get_soup(url)
    urls = ['https://www.titan.fitness/strength/weight-plates/' + a['href'] for a in soup('a', 'gtm-product-list')]
    with ThreadPoolExecutor(max_workers=len(urls)) as pool:
        results = pool.map(get_availability_plates, urls)
    results = sum(results, [])
    results = pd.DataFrame(results)
    print(results)
    
        
    
if __name__ == "__main__":
    main()
