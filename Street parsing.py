import requests
from bs4 import BeautifulSoup
import csv


URL = 'http://wikimapia.org/street/18269308/ru/%D0%B4%D0%B5%D1%80-%D0%AF%D1%81%D0%B5%D0%BD%D0%BA%D0%B8'
HEADERS = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36', 'accept': '*/*'}
FILE = 'houses2.csv'
list = ['И-521а', 'И-522а', 'И-700А', 'И-700А Ясенево', 'И-760А', 'И-491а', 'И-III-3', 'КОПЭ', 'КОПЭ-М-Парус', 'КОПЭ-Башня', 'П-42', 'П-43', 'П-44', 'П-44К', 'П-44М', 'П-44Т', 'П-44ТМ/25 (ТМ-25)', 'П-55', 'П-55М', 'ПД-1', 'ПД-3', 'ПД-4', '1МГ-600', '1МГ-601', '1МГ-601-441', '1МГ-601Д', '1МГ-601Е', '1МГ-601Ж', 'II-18/12 Б', 'II-20', 'II-67 «Москворецкая»', 'II-67 Смирновская', 'II-67 Тишинская', 'II-68-01/12-83', 'II-68-01/16', 'II-68-02/12К', 'II-68-02/16М', 'II-68-03', 'II-68-04', 'Башня Вулыха', 'П-3', 'П-4', 'П-22К', 'П-3М', 'II-28', 'II-29', 'II-29-Б', 'П-30', 'II-49', 'II-57', 'И-155', 'И-155MK', 'И-155MМ', 'И-155Н', 'И-155-Б', 'И-209а', '1605-АМ/5', '1605-АМ/9,1605-АМ/12', 'П-46', 'П-46М', 'П-47', 'П-111М', 'Бекерон', 'ГМС-1 (ГМС-2001)', 'ГМС-3', 'ЕвроПа', 'II-01', 'II-02', 'II-03', 'II-04', 'II-05', 'II-08', 'II-14', 'СМ-1', 'СМ-3, СМ-6', '1МГ-300', 'К-7', 'II-18-01/08Б,II-18-01/09Б', 'II-18-01/08МИК,09МИК', '1-335', '1-410', '1-447', '1-510', '1-511', '1-513', '1-515/5', '1-515/9М', 'Колос', 'C-222', 'C-220', 'Юбилейный', 'Юникон', 'Призма (И-1630)', 'И-1723', 'И-1724', 'И-79-99', 'ИП-46С', 'И-1782', 'МЭС-84', 'БОД-1', 'Айсберг', 'И-1414', 'II-66', 'Лебедь']


#Get a response from a page
def get_html (url):
    r = requests.get(url, headers=HEADERS)
    return r


#Parsing a page
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    #Among all the content of the page, we are looking for li c class_="tagscl"
    items = soup.find_all('li', class_="tagscl")

    links = []
    for item in items:
        #Among all the content of the items, we are looking for "data-rel" : "place" and get the links to buildings
        links.append(item.find(attrs={"data-rel": "place"}).get('href'))
    return links


#Read each of the received links
def read_link (URL):
    r = get_html (URL)
    soup = BeautifulSoup(r.text, 'lxml')
    #Among all the content of the page, we are looking for div c id="place-description"
    placeinfo = soup.find_all('div', id="place-description")
    for i in placeinfo:
        return i.text.replace('\n','')

#Get the street name and house number
def street_house (URL):
    r = get_html(URL)
    soup = BeautifulSoup(r.text, 'lxml')
    #Among all the content of the page, we are looking for "data-rel": "street"
    street = soup.find(attrs={"data-rel": "street"}).get_text()
    house_num = soup.find('address').get_text().split(',')[-1]
    house_num = house_num.replace('\n','')
    house_num = ' '.join(house_num.split())
    return street, house_num

#Save to *.csv file
def save_file(items,path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Street', 'House', 'Description','Type'])
        for item in items:
            writer.writerow([item['street'], item['house_num'], item ['desc'],item ['type']])

#Looking for the correspondence between the received data and the list with a series of houses
def find_type (list, descr):
    for i in list:
        if descr.find(i) != -1:
            return i
        else:
            pass

#Main function
def parse ():
    html = get_html(URL)
    if html.status_code == 200:
        links = get_content(html.text)
        fin = []
        for i in links:
            if read_link(i) != None:
                street, house_num = street_house(i)
                fin.append({
                    'street': street,
                    'house_num': house_num,
                    'desc': read_link(i),
                    'type': find_type(list, read_link(i)),
                        })
        save_file(fin, FILE)
    else:
        print('Error')


parse()