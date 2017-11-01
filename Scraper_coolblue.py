from lxml import html
import requests
from bs4 import BeautifulSoup as soup

def scrape(url):


	product_categorie = url[(url.find('producttype:')+12):]
	filename = "producten.csv"
	f = open(filename, "a")

	hoofdingen = "product_name; Link; Fabrikantcode; Prijs\n"

	f.write(product_categorie + "\n")
	f.write(hoofdingen)

	#Alle html code van de pagina halen en omzetten naar soup
	website = requests.get(url)
	pagina_html = website.text
	pagina_soup = soup(pagina_html, "html.parser")

	#zoeken hoe veel paginas er zijn voor dit product
	paginas = pagina_soup.findAll("a",{"class":"pagination__content"})
	allepagination = len(paginas)
	aantal_paginas = int(paginas[allepagination-2].text.strip())

	#over elke pagina gaan van 1 soort product
	for c in range(1, (aantal_paginas + 1)):
		url = url + "?pagina=" + str(c)
		
		website = requests.get(url)
		pagina_html = website.text
		pagina_soup = soup(pagina_html, "html.parser")

		naamcontainer = pagina_soup.findAll("a",{"class":"product__title js-product-title"})
		prijscontainer = pagina_soup.findAll("strong",{"class":"product__sales-price"})

		#Naam, prijs en link naar productpagina uit container halen
		hoeveel = len(naamcontainer)
		product_href = {}
		product_page = {}
		item_Prijs = {}
		item_name = {}

		for i in range(0, hoeveel):
			item_name[i] = naamcontainer[i].text.strip()

			product_href[i] = naamcontainer[i]["href"].replace("https://www.coolblue.be", "")
			product_page[i] = "https://www.coolblue.be" + product_href[i]

			item_Prijs[i] = prijscontainer[i].text.strip()

		#Op elke productpagina de juiste gegevens halen
		product_website = {}
		product_html = {}
		product_soup = {}
		item_specificaties = {}
		item_Artikelnr = {}

		for i in range(0, hoeveel):
			product_website[i] = requests.get(product_page[i])
			product_html[i] = product_website[i].text
			product_soup[i] = soup(product_html[i], "html.parser")

			item_specificaties[i] = product_soup[i].findAll("dd",{"class":"product-specs__item-spec"})
			item_Artikelnr[i] = item_specificaties[i][5].text.strip()

		for i in range(0, hoeveel):
			print("Naam: " + item_name[i])
			print("Link: " + product_page[i])
			print("artikelnr: " + item_Artikelnr[i])

			f.write(item_name[i] + ";" + product_page[i] + ";" + item_Artikelnr[i] + ";" + item_Prijs[i] + "\n")	
		url = url.replace("?pagina="+str(c), "")
	f.close()
	
url = ['https://www.coolblue.be/nl/computer-onderdelen/producttype:solid-state-drives-ssd', 'https://www.coolblue.be/nl/computer-onderdelen/producttype:processoren', 'https://www.coolblue.be/nl/computer-onderdelen/producttype:interne-harde-schijven', 'https://www.coolblue.be/nl/producttype:monitoren']
for i in range(0, len(url)):
	scrape(url[i])