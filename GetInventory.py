import MySqlConnector
import json

#Function to retrieve all the articles in inventory
def getAllInventory():
    sqlQuery = "SELECT art_id, name, stock from inventory"

    sqlOutput = MySqlConnector.mysqlExecutor(sqlQuery)

    articlesList = []

    for article in sqlOutput:
        #Creating a dict object for each article
        articleList = {"art_id": article[0], "name": article[1], "stock": article[2]}
        #Pushing The dict object in a List, creating a List of dictionary.
        articlesList.append(articleList)

    #Converting LIst of dict into json since, List is not a valid response object for HTTP/API
    allInventoryJson = json.dumps(articlesList)

    return allInventoryJson