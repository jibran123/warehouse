import JsonReader
import MySqlConnector
import MySqlUtility

#Adding/Updating Inventory, based on the file uploaded
def addInventory(inputJsonFile):
    inventoryObject = JsonReader.readInventory(inputJsonFile)

    #If the JSON doesn't have `Inventory` Object, then return False. Failing the Update Inventory.
    if inventoryObject == False:
        return "False"

    for inventory in inventoryObject:
        #Check the the article is new or already exists in inventory
        articleExists = MySqlUtility.checkArticleExists(str(inventory['art_id']))
        failedUpdate = []

        #If Exists then following code will update the article w.r.t art_id
        if articleExists == "1":
            currentStockCount = MySqlUtility.getStockCount(str(inventory['art_id']))
            newStockCount = currentStockCount + int(inventory['stock'])

            sqlQuery = "UPDATE inventory SET stock=%s WHERE art_id=%s AND name=%s"
            vals = (newStockCount, inventory['art_id'], inventory['name'])

            sqlOutput = MySqlConnector.mysqlExecutor(sqlQuery, vals)

            #Check if UPdate is successful. else note the inventory article name
            if sqlOutput != 1:
                failedUpdate.append(inventory['name'])

        #If Article is new then following code will add the new article.
        else:
            sqlQuery = "INSERT INTO inventory (art_id, name, stock) VALUES (%s, %s, %s)"
            vals = (inventory['art_id'], inventory['name'], inventory['stock'])

            sqlOutput = MySqlConnector.mysqlExecutor(sqlQuery,vals)

            #Check if Addition of New Article is successful. else note the inventory article name
            if sqlOutput != 1:
                failedUpdate.append(inventory['name'])

    #Checking if all add/update is successful, if it is successful return True, else return False
    if len(failedUpdate) > 0:
        return "False"

    else:
        return "True"