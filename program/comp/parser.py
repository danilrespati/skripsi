from bs4 import BeautifulSoup
import urllib.request
import cv2

def initUrl():
    url = 'http://192.168.100.13/skripsi/target.php'
    web = urllib.request.urlopen(url)
    html = web.read()
    soup = BeautifulSoup(html, 'lxml')
    return soup
          
soup = initUrl()

stat = soup.find('em').text
target = soup.find('td', {'id' : 'target'}).text
x = soup.find('td', {'id' : 'x'}).text
y = soup.find('td', {'id' : 'y'}).text

print(stat, target, x,y)
