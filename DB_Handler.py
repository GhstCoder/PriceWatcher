import mysql.connector

cnx = mysql.connector.connect(user='root'), password='root', host="127.0.0.1", pricewatcher_db)

def insertData(WebshopID, productName, productPrice, ScrapeTimestamp, EAN, Productcode, ProductURL):
    cursor = cnx.cursor()
    #Komma in prijs vervangen door punt (nodig voor correcte insert in db)
    productPrice = productPrice.replace(",",".")

    #Als geen EAN werd meegegeven, zoek product a.d.h.v. Productcode
    if not EAN:
        query_checkProduct = ('SELECT * FROM product WHERE fabrikantCode = %s', Productcode)
        cursor.execute(query_checkProduct)

        #Als het product nog niet bestaat, maak dan nieuw product aan
        if cursor.rowcount == 0:
            query_addProduct = ('INSERT INTO product (Fabrikantcode, Naam, Prijs, ProductCategorieID) \
                                VALUES (%s, %s, %d, %i)' % (Productcode, productName, productPrice, ))
            #Nogmaals zoeken om productID te kunnen achterhalen
            cursor.execute(query_checkProduct)
        #Selecteer productID uit db
        productID = cursor.fetchone()[0]
        query_addPrice = ('INSERT INTO productwebshop (WebshopID, ProductID, Prijs, ProductUrl) \
                           VALUES (%i, %i, %f, %s)' % (WebshopID, productID, productPrice, ProductUrl))
        #Prijs toevoegen aan db
        cursor.execute(query_addPrice)
    #Als geen ProductCode werd meegegeven, ofwel wel een EAN zoek a.d.h.v. EAN
    else:
        query_checkProduct = ('SELECT * FROM product WHERE EAN = %s' % EAN)


cnx.close()
