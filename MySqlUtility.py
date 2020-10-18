import MySqlConnector

#Get the current stock count for an article.
def getStockCount(art_id):
    sqlQuery = "SELECT stock FROM inventory WHERE art_id=\"{}\";".format(art_id)

    sqlOutput = MySqlConnector.mysqlExecutor(sqlQuery)

    return sqlOutput[0][0]

#Check if a product already exists in Database
def checkProductExists(productName):
    sqlQuery = "SELECT ProductName FROM allproducts WHERE ProductName=\"{}\";".format(productName)

    sqlOutput = MySqlConnector.mysqlExecutor(sqlQuery)

    return str(len(sqlOutput))

#Update Inventory, post Buying a product
def updateStock(art_id, updatedStock):
    sqlQuery = "UPDATE inventory SET stock=%s WHERE art_id=%s"
    vals = (updatedStock, art_id)

    sqlOutput = MySqlConnector.mysqlExecutor(sqlQuery, vals)

    return sqlOutput

#Get All Product Names from Database
def getAllProductNames():
    sqlQuery = "SELECT DISTINCT ProductName FROM allproducts"

    sqlOutput = MySqlConnector.mysqlExecutor(sqlQuery)

    productArray = []

    for product in sqlOutput:
        productArray.append(product[0])

    return(productArray)

#Check If an article already exists in Database
def checkArticleExists(art_id):
    sqlQuery = "SELECT art_id FROM inventory WHERE art_id={};".format(art_id)

    sqlOutput = MySqlConnector.mysqlExecutor(sqlQuery)

    return str(len(sqlOutput))