import json

#Utitilty To Read the Json file for Inventory
def readInventory(inputJsonFile):
    with open(inputJsonFile) as jsonFile:
        jsonData = json.load(jsonFile)
        jsonFile.close()

    #Check if inventory is an object in JSON. If yes then return the JSON `inventory` object
    if "inventory" in jsonData:
        inventoryList = jsonData['inventory']

        return inventoryList

    #If Not then return false, so that upload Inventory function can send a Failure message to user
    return False

#Utitilty To Read the Json file for Products
def readProducts(inputJsonFile):
    with open(inputJsonFile) as jsonFile:
        jsonData = json.load(jsonFile)
        jsonFile.close()

    #Check if product is an object in JSON. If yes then return the JSON `product` object
    if "products" in jsonData:
        productList = jsonData['products']

        return productList

    #If Not then return false, so that upload Product function can send a Failure message to user
    return False