'use strict';

var app = angular.module("warehouse", ["ngRoute", "smart-table"]);

app.controller("manageInventoryController", function($scope, $http, $log){
  $scope.uploadMessage = '';
  $scope.uploadButton = false;
  $scope.uploadFile = function(files) {
    $scope.uploadMessage = '';
    $scope.file = new FormData();
    $scope.file.append("file", files[0]);
    $scope.uploadButton = files.length > 0 ? true : false;
    $scope.$apply();
  };
  $scope.uploadInventory= function() {
    $http.post('/uploadInventory', $scope.file, {
          headers: {'Content-Type': undefined },
          transformRequest: angular.identity
        }).success(function(results)
          {
            if(results == 'True'){
              $scope.uploadMessage = 'Inventory Updated Successfully';
            }else if(results == 'False'){
              $scope.uploadMessage = 'Inventory Updated Failed';
            }
            $scope.getInventory();
          }).error(function(error)
          {
            $log.log(error);
          });
      };

      $scope.getInventory = function() {
        $http.get('/getAllInventory').success(function(results){
          $scope.inventory = [];
          angular.forEach(results, function(key, value){
            var tmp = {
              art_id : key["art_id"],
              art_name : key["name"],
              availableCount : key["stock"]
            }
            $scope.inventory.push(tmp);
          })
          $scope.uploadButton = false;
        }).error(function(error){
            $log.log(error);
        });
      };
      $scope.getInventory();
  });

  app.controller("manageProductController", function($scope, $http, $log){
    $scope.uploadMessage = '';
    $scope.uploadButton = false;
    $scope.uploadFile = function(files) {
      $scope.uploadMessage = '';
      $scope.file = new FormData();
      $scope.file.append("file", files[0]);
      $scope.uploadButton = files.length > 0 ? true : false;
      $scope.$apply();
    };
    $scope.uploadProduct= function() {
      $http.post('/uploadProduct', $scope.file, {
            headers: {'Content-Type': undefined },
            transformRequest: angular.identity
          }).success(function(results){
              if(results == 'True'){
                $scope.uploadMessage = 'Products Updated Successfully';
              }else if(results == 'False'){
                $scope.uploadMessage = 'Products Update Failed';
              }
              $scope.uploadButton = false;
              $scope.getProducts();
            }).error(function(error){
              $log.log(error);
            });
        };

        $scope.getProducts = function() {
          $http.get('/getAllProducts').success(function(results){
            $scope.products = [];
            angular.forEach(results, function(key, value){
              $scope.products.push({"productName":value });
            })
            $scope.uploadButton = false;
          }).error(function(error){
              $log.log(error);
          });
        };
        $scope.getProducts();
    });

  app.controller("purchaseController", function($scope, $http, $log, $rootScope){
    $scope.loading = false;
    $scope.buyMessage = "";
    $scope.isProductSelected = false;
    $scope.availableProducts = [];
    $scope.getProductWithCount = function(){
        $scope.isProductSelected = false;
        $http.get('/getAllProducts').success(function(results){
          $scope.products = results;
          $http.get('/getAllInventory').success(function(results){
            $scope.inventory = results;
            $scope.calculateAvailableProducts($scope.products, $scope.inventory, "");
          }).error(function(error){
              $log.log(error);
          });
        }).error(function(error){
          $log.log(error);
        });
    };
    $scope.getProductWithCount();

    $scope.decrement = function(product) {
      var index = $scope.availableProducts.findIndex(({productName}) => productName == product.productName);
      $scope.availableProducts[index].itemSelected--;
      $scope.updateAvailableProducts('remove', $scope.availableProducts[index].productName);
    };

    $scope.increment = function(product) {
      $scope.isProductSelected = true;
      $scope.buyMessage = '';
      var index = $scope.availableProducts.findIndex(({productName}) => productName == product.productName);
      $scope.availableProducts[index].itemSelected++;
      $scope.updateAvailableProducts('add', $scope.availableProducts[index].productName);
    };

    $scope.calculateAvailableProducts = function(prod, inv, selectedItems){
      $scope.availableProducts = [];
        angular.forEach(prod, function(key, value) {
          var product = {
            productName : value,
            productCount : -1,
            itemSelected : selectedItems[value] == undefined ? 0 : selectedItems[value]
          }
          angular.forEach(key, function(aKey, aValue){
            var requiredInventory = aKey;
            var inventoryStock = inv.find( ({ art_id }) => art_id === requiredInventory["art_id"]);
            if(product.productCount == -1){
              product.productCount = (inventoryStock["stock"] >= requiredInventory["stockRequired"]) ? Math.floor(inventoryStock["stock"] / requiredInventory["stockRequired"]) : 0; //UPdated JP
            }else {
              product.productCount = (product.productCount > (inventoryStock["stock"] / requiredInventory["stockRequired"])) ? Math.floor(inventoryStock["stock"] / requiredInventory["stockRequired"]) :  product.productCount;
            }
          });
          $scope.availableProducts.push(product);
        });
    };

    $scope.updateAvailableProducts = function(operation, productRef){
      var selectedItems = {};
      angular.forEach($scope.availableProducts, function(key, value){
        if(key.itemSelected > 0){
          selectedItems[key.productName] = key.itemSelected;
        }
      })
      if(JSON.stringify(selectedItems) === '{}'){
        $scope.isProductSelected = false;
        $scope.getProductWithCount();
      }else{
        angular.forEach($scope.products[productRef], function(pkey, pValue) {
            for(var i in $scope.inventory){
              if($scope.inventory[i]["art_id"] == pkey["art_id"]) {
                if(operation == 'add'){
                  $scope.inventory[i]["stock"] -= (pkey["stockRequired"] * 1);
                }else if(operation == 'remove') {
                  $scope.inventory[i]["stock"] += (pkey["stockRequired"] * 1);
                }
              }
            }
        });
        $scope.calculateAvailableProducts($scope.products, $scope.inventory, selectedItems);
      }
    };

    $scope.buyProducts = function(){
      $http.post('/buyProduct', $scope.inventory).success(function(results){
          if(results === 'True')$scope.buyMessage = "Products Purchased Successfully";
          $scope.getProductWithCount();
        }).error(function(error){
          $log.log(error);
        });
    };
  });

app.config(function($routeProvider) {
    $routeProvider
    .when("/inventory", {
      templateUrl : "../static/html/inventory.html",
      controller: "manageInventoryController"
    }).when("/product", {
      templateUrl : "../static/html/product.html",
      controller: "manageProductController"
    }).otherwise({
        templateUrl : "../static/html/availableProducts.html",
        controller: "purchaseController"
    });
  });

