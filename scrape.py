from urllib.request import Request, urlopen      
from bs4 import BeautifulSoup
import re
import sys

#Classe Car será utilizada posteriormente.
class Car:
    def __init__(self, name, price, mileage, exchange, url):
        self.name = name
        self.price = price
        self.mileage = mileage
        self.exchange = exchange
        self.url = url

def jumpBetweenPages(lastPageNum,site,carName):
    num = int(lastPageNum[0])
    i=2
    while(num >= i):
        newpage = site
        newpage = newpage+"?o={}&q={}".format(i,carName)
        i+=1
        bsObj = request(newpage)
        getContent(bsObj)

def getContent(bsObj):
    names = bsObj.find_all("h2",{"class":"sc-1mbetcw-0 fKteoJ sc-ifAKCX jyXVpA"})
    prices = bsObj.find_all("span",{"class":"sc-ifAKCX eoKYee"})
    infos = bsObj.find_all("span",{"class":"sc-1j5op1p-0 lnqdIU sc-ifAKCX eLPYJb"})
    urls = bsObj.find_all("a",{"class":"fnmrjs-0 fyjObc"})
    listCars(names,prices,infos,urls)

def listCars(names,prices,infos,urls):
    listOfCars = []
    for name, price, info, url in zip(names,prices,infos,urls):
        urlhref = url['href']
        carName = name.get_text()
        carPrice = price.get_text()
        exchange = ""
        try:
            mileage, exchangeInfo, gasType = info.get_text().split("|")
        except:
            try:
                mileage, exchangeInfo = info.get_text().split("|")
                exchange = exchangeInfo.split(": ")[1]
            except:
                mileage = info.get_text()

        listOfCars.append(Car(carName, carPrice, mileage, exchange, urlhref))

        print(f"Name of the car:{carName}\nPrice:{carPrice}\nMileage:{mileage}\nExchange:{exchange}\nUrl:{urlhref}\n --------------------------------------------------------------")


def request(site):
    hdr = {'User-Agent':'Mozilla/5.0'}
    req = Request(site, headers=hdr)
    html = urlopen(req)
    bsObj = BeautifulSoup(html, features="html.parser")
    return bsObj

def main():
    site = sys.argv[1]
    carName = input("Digite o carro que deseja buscar: ")
    firstPage = site+"?q={}".format(carName)
    bsObj = request(firstPage)
    lastPageNum = bsObj.find("a",{"class":"sc-1bofr6e-0 iRQkdN","data-lurker-detail":"last_page"})
    lastPageNum = re.findall(r'\d+', lastPageNum['href'])

    getContent(bsObj)
    jumpBetweenPages(lastPageNum,site,carName)


main()

        
        