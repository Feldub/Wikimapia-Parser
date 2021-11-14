import requests
from bs4 import BeautifulSoup

URL = 'http://tipdoma.ru/list1.html'
HEADERS = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36', 'accept': '*/*'}

#Get a response from a page
def get_html (url):
    r = requests.get(url, headers=HEADERS)
    r.encoding = 'utf8'
    return r

#Parsing a page
def read_link (URL):
    list =[]
    r = get_html(URL)
    soup = BeautifulSoup(r.text, 'lxml')
    #Among all the content of the page, we are looking for div c class_='caption'
    type = soup.find_all('div', class_='caption')
    #There can be several elements with the same class, a list of elements will be returned. In order to view each element, we go through the list using an iterable list
    for i in type:
        list.append(i.find('h4').text)
    print(list)

def pars ():
    read_link(URL)

pars()


