#!/bin/bash
mongoimport --drop --host database --db grocery_store --collection customers --type csv --file /data/customers_mongo.csv --headerline
mongoimport --drop --host database --db grocery_store --collection products --type csv --file /data/products_mongo.csv --headerline
mongoimport --drop --host database --db grocery_store --collection categories --type csv --file /data/categories_mongo.csv --headerline
mongoimport --drop --host database --db grocery_store --collection orders --type csv --file /data/orders_mongo.csv --headerline
mongoimport --drop --host database --db grocery_store --collection order_product --type csv --file /data/order_product_mongo.csv --headerline