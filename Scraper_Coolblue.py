from lxml import html
import requests
from bs4 import BeautifulSoup as soup

url = "https://www.coolblue.be/nl/zoeken/producttype:processoren/processormerk:intel?query=processoren"

website = requests.get(url)
pagina_html = website.text
pagina_soup = soup(pagina_html, "html.parser")

containers = pagina_soup.findAll("a",{"class":"product__title js-product-title"})

product_name = containers[0].text.strip()

product_page = "https://www.coolblue.be" + containers[0]["href"]
product_page = requests.get(product_page)

