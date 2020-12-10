from bs4 import BeautifulSoup
import urllib.request
import time


def initUrl():
    url = 'http://192.168.0.120/skripsi/target.php'
    web = urllib.request.urlopen(url)
    html = web.read()
    soup = BeautifulSoup(html, 'lxml')
    stat = soup.find('em').text
    target = soup.find('td', {'id': 'target'}).text
    pan = soup.find('td', {'id': 'pan'}).text
    tlt = soup.find('td', {'id': 'tlt'}).text
    return stat, target, float(pan), float(tlt)


servo = {"pan": 13, "tlt": 11}
angle = {"pan": 0, "tlt": 0}
currAngle = {"pan": 0, "tlt": 0}
while True:
    stat, target, angle["pan"], angle["tlt"] = initUrl()
    if target == "Speedtest":
        print(time.time())
        break
