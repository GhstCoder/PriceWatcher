from lxml import html
import requests
from bs4 import BeautifulSoup as soup

#file genereren
filename = 'products.csv'
f = open(filename, 'w')
headers = "product_name; EAN; fabrikantCode; price; productUrl\n"
f.write(headers)

#Array met te scrapen links
allLinks = ['https://www.alternate.be/Hardware/Processoren/Intel',
'https://www.alternate.be/Hardware/Processoren/AMD',
'https://www.alternate.be/Beeld-Geluid/Monitoren/Alle-monitoren',
'https://www.alternate.be/Hardware/Harde-schijven-intern/SATA',
'https://www.alternate.be/Hardware/SSDs/Alle-SSDs']
brands = ['CPU - Intel', 'CPU - AMD', 'Monitoren', 'HDD - Intern', 'SSD']

for j in range(len(allLinks)):

    f.write(brands[j]+"\n")
    #Te scrapen link
    link = allLinks[j]

    #Ophalen pagina van link
    page = requests.get(link)
    page_soup = soup(page.text, 'html.parser')

    #Meedere pagina's vinden
    morePages = page_soup.findAll('div',{'class':'paging'})
    thePages = morePages[0].findAll('a')
    allPages = len(thePages) - 2
    lastPage = thePages[allPages].text

    #Loopen door meerdere pagina's
    for i in range(1, (int(lastPage)+1)):
        #ophalen pagina van (nieuwe)link
        pageLink = link + '&page=' + str(i)
        page = requests.get(pageLink)
        page_soup = soup(page.text, 'html.parser')

        #alle producten op pagina vinden
        containers = page_soup.findAll('div',{'class':'listRow'})

        #Loop om door alle gevonden producten te gaan
        for b in range (len(containers)):
            item = containers[b]
            #prijs opslaan
            priceContainer = item.findAll('span', {'class':'price right right10'})
            price = priceContainer[0].text.replace('*', '')
            newLink = item.a["href"]

            #Nieuwe pagina van product details
            productUrl = link+newLink
            newPage = requests.get(productUrl)
            newPage_soup = soup(newPage.text, 'html.parser')

            #Product naam selecteren
            helpContainers = newPage_soup.findAll('h1')
            productName = helpContainers[0].findAll('span')[1].text

            #Product details selecteren
            newContainers = newPage_soup.findAll('div', {'class':'techData'})
            details = newContainers[0].findAll('td', {'class':'c4'})

            #switch-like proces om informatie op juiste plaats op te halen
            if (j == 0) or (j == 1):
                EAN = details[1].text
                fabrikantCode = details[2].text
                #Als EAN niet bestaat, maak leeg en lees juiste waarde fabrikantCode in
                if any(c.isalpha() for c in EAN) == True:
                    EAN = ''
                    fabrikantCode = details[1].text
            elif (j == 2):
                #Zoek voor EAN en fabrikantCode
                k = 0
                while True:
                    EAN = details[k].text
                    fabrikantCode = details[k+1].text
                    k += 1
                    if any(c.isalpha() for c in EAN) == False:
                        break
            elif (j == 3):
                EAN = details[1].text
                fabrikantCode = details[2].text
                if any(c.isalpha() for c in EAN) == True:
                    EAN = ''
                    fabrikantCode = details[1].text
                #fabrikantcode staat in naam als 'inch' als fabrikantcode werd gegeven
                if 'inch' in fabrikantCode:
                    fabrikantCode = productName.split()
                    if 'TB' in fabrikantCode[0]:
                        fabrikantCode = fabrikantCode[1]
                    else:
                        fabrikantCode = fabrikantCode[0]
            elif (j == 4):
                try:
                    EAN = details[1].text
                    fabrikantCode = details[2].text
                    if any(c.isalpha() for c in EAN) == True:
                        EAN = details[2].text
                        fabrikantCode = details[3].text

                except IndexError:
                    "skipped"

            #Schrijven naar file
            f.write(productName + ";" +  EAN + ";" + fabrikantCode + ";" + price + ";" + productUrl +"\n")

f.close()
