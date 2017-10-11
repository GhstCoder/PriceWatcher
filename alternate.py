from lxml import html
import requests
from bs4 import BeautifulSoup as soup

#file genereren
filename = 'products.csv'
f = open(filename, 'w')
headers = "product_name; EAN; fabrikantCode\n"
f.write(headers)

#Te scrapen link
link = 'https://www.alternate.be/Hardware/Processoren/Intel'

#Ophalen pagina van link
page = requests.get(link)
page_soup = soup(page.text, 'html.parser')

#alle producten op pagina vinden
containers = page_soup.findAll('div',{'class':'listRow'})

#Enkel 1e product bekijken en link naar product pagina selecteren
item = containers[0]
newLink = item.a["href"]

#Nieuwe pagina van prduct details
newPage = requests.get(link+newLink)
newPage_soup = soup(newPage.text, 'html.parser')

#Product naam selecteren
helpContainers = newPage_soup.findAll('h1')
productName = helpContainers[0].findAll('span')[1].text

#Product details selecteren
newContainers = newPage_soup.findAll('div', {'class':'techData'})
details = newContainers[0].findAll('td', {'class':'c4'})

EAN = details[1].text
fabrikantCode = details[2].text

#Schrijven naar file
f.write(productName + ";" +  EAN + ";" + fabrikantCode + "\n")

f.close()
