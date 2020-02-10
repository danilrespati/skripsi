from bs4 import BeautifulSoup
import urllib.request

class url:
    def __init__(self, url):
        self.web = urllib.request.urlopen(url)

    def parse(self):
        html = self.web.read()
        soup = BeautifulSoup(html, 'lxml')
        stat = soup.find('em').text
        target = soup.find('td', {'id': 'target'}).text
        anglePan = soup.find('td', {'id': 'x'}).text
        angleTlt = soup.find('td', {'id': 'y'}).text
        return stat, target, anglePan, angleTlt