from urllib.request import Request, urlopen      
from bs4 import BeautifulSoup
from .models import Car
import re
import itertools


def jumpBetweenPages(lastPageNum,site,carName):
    num = int(lastPageNum[0])
    i=2
    while(num >= i):
        newpage = site
        newpage = newpage+"?o={}&q={}".format(i,carName)
        i+=1
        bsObj = request(newpage)
        getContent(bsObj, carName)

def getContent(bsObj, carName):
    names = bsObj.find_all("h2",{"class":"sc-1mbetcw-0 fKteoJ sc-ifAKCX jyXVpA"})
    prices = bsObj.find_all("span",{"class":"sc-ifAKCX eoKYee"})
    infos = bsObj.find_all("span",{"class":"sc-1j5op1p-0 lnqdIU sc-ifAKCX eLPYJb"})
    urls = bsObj.find_all("a",{"class":"fnmrjs-0 fyjObc"})
    imgs = bsObj.find_all("img",{"class":"sc-101cdir-1 fwpxEI","class":"sc-101cdir-0 cldTqT"})
    listCars(names,prices,infos,urls,imgs, carName)

def listCars(names,prices,infos,urls,imgs,searchedCar):
    listOfCars = []
    for name, price, info, url, img in itertools.zip_longest(names,prices,infos,urls,imgs,fillvalue=""):
        
        try:
            nameComparison = name.get_text().lower()
        except :
            nameComparison = name.lower()

        if searchedCar in nameComparison:
            urlhref = url['href']
            carName = name.get_text()
            carPrice = price.get_text()
            exchangeInfo = ""
            try:
                imagePath = img['data-src']
            except :
                imagePath = img['src']
        else:
            continue

        try:
            mileage, exchangeInfo, gasType = info.get_text().split("|")
        except:
            try:
                mileage, exchangeInfo = info.get_text().split("|")
                exchangeInfo = exchangeInfo.split(": ")[1]
            except:
                mileage = info.get_text()

        print(f"Name of the car:{carName}\nPrice:{carPrice}\nMileage:{mileage}\nExchange:{exchangeInfo}\nUrl:{urlhref}\nImage:{imagePath}\n--------------------------------------------------------------")
        Car.objects.create(name=carName, price=carPrice,mileage=mileage,
                            exchange=exchangeInfo,url= urlhref,img=imagePath)

def request(site):
    hdr = {'User-Agent':'Mozilla/5.0'}
    req = Request(site, headers=hdr)
    html = urlopen(req)
    bsObj = BeautifulSoup(html, features="html.parser")
    return bsObj

def main(name):
    site = "https://ba.olx.com.br/grande-salvador/autos-e-pecas/carros-vans-e-utilitarios"
    carName = name.lower()
    firstPage = site+"?q={}".format(carName)
    bsObj = request(firstPage)
    lastPageNum = bsObj.find("a",{"class":"sc-1bofr6e-0 iRQkdN","data-lurker-detail":"last_page"})
    lastPageNum = re.findall(r'\d+', lastPageNum['href'])
    getContent(bsObj,carName)
    jumpBetweenPages(lastPageNum,site,carName)


        
        