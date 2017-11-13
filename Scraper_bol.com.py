## By: GhstCoder
# imports the required modules
# we use this module for aquiring the webpage
from urllib.request import urlopen as uReq
import urllib.error
# this module makes it easier to retrieve data out of the webpage
from bs4 import BeautifulSoup as soup

# Defines the functions
# returns the parsed webpage
def getHTMLPage(URL):
    # Sends a HTML request and saves it
    uClient = uReq(URL)
    # Reads the HTML response and saves it
    pageHtml = uClient.read()
    # Closes the connection
    uClient.close()
    return pageHtml
# returns the data we need for the products
def getProductName(htmlPage, index):
    # html parsing
    parsedPage = soup(htmlPage, 'html.parser')
    productName = parsedPage.findAll('a', {'class':'product-title'})[index].string
    # Encodes the string to ascii and decodes it back to utf-8 to remove special characters
    # that can cause problems
    productName = (productName.encode('ascii', 'ignore')).decode("utf-8")
    # Removes the double ' ' characters and returns the result
    return ' '.join(productName.split())
def getProductPrice(htmlPage, index):
    # html parsing
    parsedPage = soup(htmlPage, 'html.parser')
    # grabs the price (format = xxx.xx)
    return parsedPage.findAll('div', {'class':'price-block__highlight'})[index].meta['content']
def getProductURL(htmlPage, index):
    # html parsing
    parsedPage = soup(htmlPage, 'html.parser')
    return parsedPage.findAll('a', {'class':'product-title'})[index]['href']
def getEAN(productURL):
    htmlPage = getHTMLPage(productURL)
    # html parsing
    parsedPage = soup(htmlPage, 'html.parser')
    # stores all the dtElements
    dtElements = parsedPage.findAll('dt', {'class':'specs__title'})

    ean_dt_index = None
    # Checks each <dt> element for the string EAN
    for i in range(len(dtElements)):
        if 'EAN' in str(dtElements[i]):
            # saves the index
            ean_dt_index = i
            break

    # gets the EAN code out of the <dd> tag, strips it from whitespaces and \n and returns it
    return parsedPage.findAll('dd', {'class':'specs__value'})[ean_dt_index].contents[0].strip()
# returns the total of products on the parsedPage
def getNumOfProductsOnPage(htmlPage):
    # html parsing
    parsedPage = soup(htmlPage, 'html.parser')
    return len(parsedPage.findAll('a', {'class':'product-title'}))
# returns the number of products on the current page -> Check on each page
def getTotalOfProducts(htmlPage):
    # html parsing
    parsedPage = soup(htmlPage, 'html.parser')
    totalProducts = parsedPage.findAll('p', {'class':'total-results'})[0].string.split(' ')[0]
    if '.' in totalProducts:
        # removes the dot from the string
        totalProducts = totalProducts.replace('.', '')
    # returns the total products as an integer
    return int(totalProducts)


# -------------------------------------------------------------------
pageCounter = 1
# This list contains the product categories and their URL's
categoryPages = [
    ['Monitors', 'Processors', 'HDD\'s', 'SSD\'s'],
    ['https://www.bol.com/nl/l/monitoren/N/10460/?page=', 'https://www.bol.com/nl/l/processoren/N/16482/?page=', 'https://www.bol.com/nl/l/externe-harde-schijven/N/7112/?page=', 'https://www.bol.com/nl/l/interne-ssd-s/N/16403/?page=']
    ]
for i in range(len(categoryPages[0])):
    # As long as there are more pages it continues
    while(True):
        try:
            htmlPage = getHTMLPage(categoryPages[1][i] + str(pageCounter))
            # Increase pageCounter
            pageCounter+=1

            # Gets all the data of a page with products
            for j in range(getNumOfProductsOnPage(htmlPage)):
                # TODO: Data in DB steken.
                # print(str(getEAN('https://www.bol.com' + getProductURL(htmlPage,i))))
                # print(getProductName(htmlPage, j))
                # print('Prijs: ' + getProductPrice(htmlPage,i))
                # print('URL: ' + getProductURL(htmlPage,i))
                # print('EAN: ' + getEAN('https://www.bol.com' + getProductURL(htmlPage,i)))
            print()
            print('Products on page: ' + str(getNumOfProductsOnPage(htmlPage)))
            print('Products in total: ' + str(getTotalOfProducts(htmlPage)))
            print()
        except urllib.error.HTTPError as e:
            print()
            print(e)
            print('No more pages!')
            print()
            break
    # Resets page pageCounter
    pageCounter=1
# -------------------------------------------------------------------
