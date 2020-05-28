#!/usr/bin/env python

import bs4
from tabulate import tabulate
import requests

def getContent(base_url):
    r=requests.get(base_url)
    data=r.text
    c=bs4.BeautifulSoup(data, "lxml")
    return c

def selectMenu():
    '''
    options={ 1: ('Clothes'), 2: ('Home Decor') }
    '''
    options_map={ 1: ('Clothes', '3-clothes'), 2: ('Home Decor', '6-home-decor') }
    for i,option in enumerate(options_map, 1):
        print("{}) {}".format(i, options_map[option][0]))
    choice = int(input("\nBrowse products:\n "))
    while choice<1 or choice>len(options_map):
        print('Please pick an option from the list')
        choice=int(input("\n Pick a category: \n"))
    return options_map[choice][1]

def buildList(base_url, option):
    complete_url=base_url + option
    content=getContent(complete_url)
    j=content.find('ul', {'class':'page-list clearfix text-sm-center'})
    p=[]
    for o in j:
        try:
            f=o.find('a', {'class':'js-search-link'}).text.strip()
            p.append(f)
        except:
            pass
    return p

def pageList(base_url, option):
    p=buildList(base_url, option)
    is_int=lambda p: p.isdigit() or (p[0] == '-' and p[1:].isdigit())
    spages=list(filter(is_int,p))
    pages=[int(i) for i in spages]
    maxpage=int(max(pages))
    minpage=int(min(pages) + 1)
    l=[]
    if maxpage == 2:
        l.append('?page=' + str(2))
    elif maxpage > 2:
        for m in range(minpage, maxpage):
            try:
                l.append('?page=' + str(m))
            except:
                pass
    return l

def buildURL(base_url, option):
    page_list=pageList(base_url, option)
    complete_url=base_url + option
    url_list=[complete_url]
    for j in page_list:
        try:
            u=complete_url + j
        except:
            pass
        url_list.append(u)
    return url_list

def showProducts(base_url, option):
    u=buildURL(base_url, option)
    # complete_url=base_url + option
    # content=getContent(complete_url)
    result=[]
    for i in u:
        try:
            content=getContent(i)
            count=1
            prod_list=content.find_all('div',{'class':'product-description'})
            for card in prod_list:
                try:
                    price=card.find('span',{'class':'price'}).text.strip()
                except:
                    pass
                try:
                    name=card.find('h2').text.replace("\n"," ").lstrip("0123456789.- ")
                except:
                    pass
                result.append([count,name,price])
                count += 1
        except:
            pass
    print(tabulate(result, headers=["Index", "Name", "Price"], tablefmt="grid"))

def main():
    base_url="http://mangafiend.com/"
    option=selectMenu()
    showProducts(base_url, option)

if __name__ == '__main__':
    main()
