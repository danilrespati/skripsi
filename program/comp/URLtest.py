from time import sleep
from bs4 import BeautifulSoup
import urllib.request

def initUrl():
    html = web.read()
    soup = BeautifulSoup(html, 'lxml')
    stat = soup.find('em').text
    target = soup.find('td', {'id': 'target'}).text
    anglePan = soup.find('td', {'id': 'x'}).text
    angleTlt = soup.find('td', {'id': 'y'}).text
    return stat, target, anglePan, angleTlt

url = 'http://192.168.100.13/skripsi/target.php'
web = urllib.request.urlopen(url)
stat, target, anglePan, angleTlt = initUrl()
print(stat, target, anglePan, angleTlt)
while (stat == "Running"):
    stat, target, anglePan, angleTlt = initUrl()
    print(target, anglePan, angleTlt)
