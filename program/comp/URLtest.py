from time import sleep
from bs4 import BeautifulSoup
import urllib.request

class url:
    def __init__(self, url):
        self.web = urllib.request.urlopen(url)

    def parse(self):
        html = web.read()
        soup = BeautifulSoup(html, 'lxml')
        stat = soup.find('em').text
        target = soup.find('td', {'id': 'target'}).text
        anglePan = soup.find('td', {'id': 'x'}).text
        angleTlt = soup.find('td', {'id': 'y'}).text
        return stat, target, anglePan, angleTlt
        
def initUrl():
    url = 'http://192.168.100.13/skripsi/target.php'
    web = urllib.request.urlopen(url)
    html = web.read()
    soup = BeautifulSoup(html, 'lxml')
    stat = soup.find('em').text
    target = soup.find('td', {'id': 'target'}).text
    anglePan = soup.find('td', {'id': 'x'}).text
    angleTlt = soup.find('td', {'id': 'y'}).text
    return stat, target, anglePan, angleTlt

com = url('http://192.168.100.13/skripsi/target.php')
stat, target, anglePan, angleTlt = url.parse()
while (stat == "Running"):
    stat, target, anglePan, angleTlt = url.parse()
    print(target, anglePan, angleTlt)
