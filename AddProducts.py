import JsonReader
import MySqlConnector
import MySqlUtility

#Function to add/update a Product, based on the JSON file pushed from UI
def addProduct(inputJsonFile):
    productObject = JsonReader.readProducts(inputJsonFile)

    #If the JSON doesn't have `products` Object, then return False. Failing the Add/Update Products.
    if productObject == False:
        return "False"

    productFailed = []

    for product in productObject:
        #Checking if Product exists.
        productExists = MySqlUtility.checkProductExists(product['name'])

        #If Product Exists, then update it's article's configuration
        if productExists != "0":
            for article in product['contain_articles']:
                sqlQuery = "UPDATE products SET amount_of=%s WHERE name=%s AND art_id=%s"
                vals = (article['amount_of'], product['name'], article['art_id'])

                sqlOutput = MySqlConnector.mysqlExecutor(sqlQuery, vals)

                #Check if Update is successful or not
                #If Successful then move to the new article/product
                if sqlOutput in (0, 1):
                    continue

                #If Update failed, then add the Product Name in the productFailed array.
                productFailed.append(product['name'])

        #If Product is new then add the product and it's configuration in the Product table.
        else:
            for article in product['contain_articles']:
                sqlQuery = "INSERT INTO products (name, art_id, amount_of) VALUES (%s, %s, %s)"
                vals = (product['name'], article['art_id'], article['amount_of'])

                sqlOutput = MySqlConnector.mysqlExecutor(sqlQuery,vals)

                #If Update failed, then add the Product Name in the productFailed array.
                if sqlOutput != 1:
                    productFailed.append(product['name'])

    #Check if the productFailed array is empty or not. If empty then all the product add/update was successful.
    #Return False if update fails else return True.
    if len(productFailed) > 0:
        return "False"

    else:
        return "True"