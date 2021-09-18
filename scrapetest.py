from urllib.request import Request, urlopen      
from bs4 import BeautifulSoup
import sys

class Car:
    def __init__(self, name, price, mileage, exchange, url):
        self.name = name
        self.price = price
        self.mileage = mileage
        self.exchange = exchange
        self.url = url

site = sys.argv[1]
carName = input("Digite o carro que deseja buscar: ")
site += site+"?q={}".format(carName)
hdr = {'User-Agent':'Mozilla/5.0'}
req = Request(site, headers=hdr)
html = urlopen(req)
bsObj = BeautifulSoup(html, features="html.parser")

names = bsObj.find_all("h2",{"class":"sc-1mbetcw-0 fKteoJ sc-ifAKCX jyXVpA"})
prices = bsObj.find_all("span",{"class":"sc-ifAKCX eoKYee"})
infos = bsObj.find_all("span",{"class":"sc-1j5op1p-0 lnqdIU sc-ifAKCX eLPYJb"})
urls = bsObj.find_all("a",{"class":"fnmrjs-0 fyjObc"})


listOfCars = []

for name, price, info, url in zip(names,prices,infos,urls):
    urlhref = url['href']
    carName = name.get_text()
    carPrice = price.get_text()
    try:
        mileage, exchangeInfo, gasType = info.get_text().split("|")
    except:
        mileage, exchangeInfo = info.get_text().split("|")
    exchange = exchangeInfo.split(": ")[1]

    listOfCars.append(Car(carName, carPrice, mileage, exchange, urlhref))

    print(f"Name of the car:{carName}\nPrice:{carPrice}\nMileage:{mileage}\nExchange:{exchange}\nUrl:{urlhref}\n --------------------------------------------------------------")






        
        