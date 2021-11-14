from xml.etree import ElementTree
import urllib.request
import time


#API link with xml data
URL = 'http://api.wikimapia.org/?key=example&function=box&coordsby=bbox&bbox=37.0%2C55.1%2C37.1%2C55.2&category=109&count=100'

#Reading an API link and getting all references to objects contained in a xml file
def reed_xml(URL):
    fileobject = urllib.request.urlopen(URL)
    tree = ElementTree.parse(fileobject)
    root = tree.getroot()
    l =[]
    for i in root.iter('url'):
        l.append(i.text)
        time.sleep(1)
    return l

print(reed_xml(URL))