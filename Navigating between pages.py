import requests
from bs4 import BeautifulSoup

URL = 'https://wikimapia.org/country/Russia/Moscow/Moscow/'
HEADERS = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36', 'accept': '*/*'}

#Get a response from a page
def get_html (url):
    r = requests.get(url, headers=HEADERS)
    return r

#Parsing a page
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a')
    links = []
    for item in items:
        #Get all links for objects on the page
        if 'http' in item['href'] and item['href'] != 'http://wikimapia.org/':
            links.append(item['href'])
    return links

#Read each of the received links
def read_link (URL):
    r = get_html (URL)
    soup = BeautifulSoup(r.text, 'lxml')
    #Among all the content of the object page, we are looking for div c id="place-description"
    placeinfo = soup.find_all('div', id="place-description")
    for i in placeinfo:
        print(i.text)

#Main function
def parse ():
    html = get_html(URL)
    if html.status_code == 200:
        links = []
        pages = 3
        for page in range (0,pages):
            print(f'Парсинг страницы {page+1} из {pages}...')
            #Link to next page
            url_new = URL + f'{page*50}/'
            html = get_html(url_new)
            links.extend(get_content(html.text))
    else:
        print('Error')
    for i in links:
        print(read_link(i))

parse()