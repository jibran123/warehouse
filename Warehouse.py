from flask import Flask, send_file, request, redirect, flash
import AddInventory, AddProducts, BuyProducts, GetInventory, GetProductStocks
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

#Location to save the uploaded file
UPLOAD_LOCATION = "/tmp"
ALLOWED_EXTENSION = "json"
app.config['UPLOAD_FOLDER'] = UPLOAD_LOCATION

#Default Page
@app.route("/")
def index():
    return send_file("templates/index.html")

#API for Uploading an Inventory
@app.route('/uploadInventory', methods=['POST'])
def uploadInventory():
    #Check if a File is passed as an Input while updating Inventory
    if 'file' not in request.files:
        flash('No file found. Please try again.')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == "":
        flash('No File Selected')
        return redirect(request.url)

    #Checking if the extension for the file name is indeed `json`
    if file and allowedFilename(file.filename):
        #Retriving the filename and location and saving the file at said location.
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        #Invoking the addInventory method with the path for newly created/saved json file
        return AddInventory.addInventory(filepath)

    #Return Failure response in case the file is not json
    return {'Invalid File Format. Expected - json. Recieved - ': file.filename}

#API for Uploading an Product
@app.route('/uploadProduct', methods=['POST'])
def uploadProduct():
    #Check if a File is passed as an Input while updating Products
    if 'file' not in request.files:
        flash('No file found. Please try again.')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == "":
        flash('No File Selected')
        return redirect(request.url)

    #Checking if the extension for the file name is indeed `json`
    if file and allowedFilename(file.filename):
        #Retriving the filename and location and saving the file at said location.
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        #Invoking the addProduct method with the path for newly created/saved json file
        return AddProducts.addProduct(filepath)

    return {'Invalid File Format. Expected - json. Recieved - ': file.filename}

#API to purchase product
@app.route('/buyProduct', methods=['POST'])
def buyProduct():
    #Converting the response object received from UI into JSON string for further processing
    updatedInventory = request.get_json()

    #Invoking the buyProduct to updated Inventory Database with the updatedInventory recieved from UI
    return BuyProducts.buyProduct(updatedInventory)

#API for getting all the inventory from Database
@app.route('/getAllInventory', methods=['GET'])
def getAllInventory():
    return GetInventory.getAllInventory()

#API for getting all the products from Database
@app.route('/getAllProducts', methods=['GET'])
def getAllProducts():
    return GetProductStocks.getAllProductsStock()

#Utility to check if the file uploaded has accepted extensions.
def allowedFilename(fileName):
      return "." in fileName and \
        fileName.rsplit('.', 1)[1].lower() == ALLOWED_EXTENSION

if __name__ == "__main__":
    app.run()