import requests
from bs4 import BeautifulSoup
import csv
from xml.etree import ElementTree
import urllib.request
import time

HEADERS = {'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36', 'accept': '*/*'}
FILE = 'houses3.csv'
categories = [109, 164, 44865] #List of required categories
box = [55.5,55.6,37.5,37.6]  #Latitude then longitude

#Get a response from a page
def get_html (url):
    r = requests.get(url, headers=HEADERS)
    return r

#Creating API links
def get_xml (categories, box):
    l =[]
    b_lat = box[2]
    while box[0] < box[1]:
        while box[2] < box[3]:
            for i in categories:
                URL_xml = f'http://api.wikimapia.org/?key=example&function=box&coordsby=bbox&bbox={round(box[2],1)}%2C{round(box[0],1)}%2C{round((box[2]+0.1),1)}%2C{round((box[0]+0.1),1)}&category={i}&count=100'
                l.append(URL_xml)
            box[2] += 0.1
        box[2] = b_lat
        box[0] += 0.1
    return l


#Getting links to buildings from the API
def reed_xml(URL):
    fileobject = urllib.request.urlopen(URL)
    tree = ElementTree.parse(fileobject)
    root = tree.getroot()
    l =[]
    for i in root.iter('url'):
        l.append(i.text)
        time.sleep(1)
    return l

#Read each of the received links
def read_link (URL):
    r = get_html (URL)
    soup = BeautifulSoup(r.text, 'lxml')
    # Among all the content of the object page, we are looking for div c id="place-description"
    placeinfo = soup.find_all('div', id="place-description")
    for i in placeinfo:
        return i.text.replace('\n','')

#Get the street name and house number
def street_house (URL):
    r = get_html(URL)
    soup = BeautifulSoup(r.text, 'lxml')
    if soup.find(attrs={"data-rel": "street"}):
        #Among all the content of the page, we are looking for "data-rel": "street"
        street = soup.find(attrs={"data-rel": "street"}).get_text()
        house_num = soup.find('address').get_text().split(',')[-1]
        house_num = house_num.replace('\n', '')
        house_num = ' '.join(house_num.split())
        return street, house_num
    else:
        return None, None

#Save to *.csv file
def save_file(items,path):
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Street', 'House', 'Description','Type'])
        for item in items:
            writer.writerow([item['street'], item['house_num'], item ['desc'],item ['type']])

#Looking for a series at home
def find_type (house_desc):
    if 'серии' in house_desc:
        house_split = house_desc.split()
        return house_split[house_split.index('серии') + 1].split('.')[0]
    elif'серия' in house_desc:
        house_split = house_desc.split()
        return house_split[house_split.index('серия') + 1].split('.')[0]
    else:
        pass

#Main function
def parse ():
    fin = []
    for l_xml in get_xml(categories, box):
        for i in reed_xml(l_xml):
            html = get_html(i)
            if html.status_code == 200:
                if read_link(i) != None:
                    street, house_num = street_house(i)
                    fin.append({
                        'street': street,
                        'house_num': house_num,
                        'desc': read_link(i),
                        'type': find_type(read_link(i)),
                            })
            else:
                print('Error')
        time.sleep(30)
    save_file(fin, FILE)


parse()