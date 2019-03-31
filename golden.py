from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
import requests
import csv

nameList = []
urlList = []
busNameList = []
numberList = []
websiteBoolList = []
countyList = []

headers = {'User-Agent': 'Mozilla/5.1 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def getDetails(content, url, county):
    global nameList
    global numberList
    global urlList
    global busNameList
    global websiteBoolList
    global countyList
    #Gets name of business
    try:
        nameStart = content.index('class="name">')
        name = content[nameStart:nameStart+100].split('>', 1)[-1]
        name = name.split("<", 1)[0]
    except:
        print("******** NAME NOT FOUND ********")
        name = "Not Found"

    if name not in nameList:
        nameList.append(name)
    else:
        return

    #Gets number of business
    try:
        numStart = content.index('"telephone">')
        number = content[numStart:numStart+100].split('>', 1)[-1]
        number = number.split("<", 1)[0]
    except:
        number = "Not Found"

    #Get website info
    webSiteTags = 0;
    webStart = ""
    try:
        webAttempt = content.index('class="contact-homepage')
        webSiteTags = 1;
        webStart = webAttempt
    except:
        pass
    if webSiteTags == 0:
        try:
            webAttempt = content.index('class="homepage icon"')
            webSiteTags = 1;
            webStart = webAttempt
        except:
            pass
    if webSiteTags == 0:
        try:
            webAttempt = content.index('class="visti_mysite"')
            webSiteTags = 1;
            webStart = webAttempt
        except:
            pass
    try:
        website = content[webStart:webStart+100].split('>', 1)[-1]
        websiteBool = "Yes"
    except:
        websiteBool = "No"

    print("***************************")
    print(url)
    print(": " + name)
    print(": " + number)
    print(": " + websiteBool)
    urlList.append(url)
    busNameList.append(name)
    numberList.append(number)
    websiteBoolList.append(websiteBool)
    countyList.append(county)

def searchPage(url):
    headers = {'User-Agent': 'Mozilla/5.1 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    try:
        response = requests.get(url, headers=headers, timeout=15)
        content = str(response.content)
        response.close()
        #Checks if the business is in Dublin
        county = ""
        try:
            content.index('Dublin')
            isDublin = True
            county = "Dublin"
        except:
            isDublin = False
        #Checks if the business is in Kildare
        try:
            content.index('Kildare')
            isKildare = True
            county = "Kildare"
        except:
            isKildare = False
        #Checks if the business is in Meath
        try:
            content.index('Meath')
            isMeath = True
            county = "Meath"
        except:
            isMeath = False

        if (isDublin == True) or (isKildare == True) or (isMeath == True):
            getDetails(content, url, county)

    except Exception as e:
        print("error" + str(e))

try:
    letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    baseUrl = 'https://www.goldenpages.ie/business/sitemap/'
    for letter in letters:
        url = baseUrl + letter
        response = requests.get(url, headers=headers, timeout=15)
        content = str(response.content)
        response.close()
        soup = BeautifulSoup(content)
        #count = 0
        allLinks = soup.findAll('a')
        businessLinks = allLinks[26:]
        for link in businessLinks:
            li = link.get('href')
            #count = count + 1
            #if count > 3:
            #    break
            searchPage('https://www.goldenpages.ie' + li)

except Exception as e:
    print("error" + str(e))

with open('potential-clients.csv', 'w') as f:
    thewriter = csv.writer(f)
    num = len(urlList)
    for i in range(0,num):
        thewriter.writerow([urlList[i],busNameList[i],numberList[i],websiteBoolList[i],countyList[i]])
