import MySqlConnector
import MySqlUtility

#Retrieve All Products with respective article configuration requirement for the products
def getAllProductsStock():
    #Get All Product Names from Database
    allProducts = MySqlUtility.getAllProductNames()

    productsAvailable = dict()

    for product in allProducts:

        sqlQuery = "SELECT art_id, StockRequired FROM allproducts where ProductName=\"{}\"".format(product)

        sqlOutput = MySqlConnector.mysqlExecutor(sqlQuery)

        productsAvailable[product] = {}
        articleList = []

        #Iterating through all the articles for the products.
        for article in sqlOutput:
            articlesTemp = {"art_id": article[0], "stockRequired": article[1]}
            #Adding all the articles in an sub dictionary object
            articleList.append(articlesTemp)

        #Adding the sub dictionary in the productsAvailable dictionary. Creating a nested dictionary.
        productsAvailable[product] = articleList

    return productsAvailable