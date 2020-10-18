import MySqlUtility

#Update Inventory as per the latest purchase order. Updated Inventory send by UI
def buyProduct(updatedInventory):
    flag = ""

    for article in updatedInventory:
        art_id = article['art_id']
        stock = article['stock']

        sqlOutput = MySqlUtility.updateStock(art_id, stock)

        #Check if the Update is successful or not
        #If not then make a note of the article name in an flag string.
        if sqlOutput in ("0", "1"):
            flag += article['name'] + " Failed to Update DB.\n"

    #If flag is empty, then all update was successful return true.
    if flag == "":
        return "True"

    #If one or more article update fails then return False, stating purchase failed.
    return "False"