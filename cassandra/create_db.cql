CREATE KEYSPACE grocery_store WITH REPLICATION = {
    'class' : 'NetworkTopologyStrategy',
    'datacenter1' : 3
    };

USE grocery_store;

CREATE TABLE IF NOT EXISTS categories
(
    id            INT PRIMARY KEY,
    category_name TEXT
);

CREATE TABLE IF NOT EXISTS products
(
    id            INT PRIMARY KEY,
    product_name  TEXT,
    price         INT,
    category_id   UUID,
    category_name TEXT
);

CREATE TABLE IF NOT EXISTS customers
(
    id      INT PRIMARY KEY,
    name    TEXT,
    surname TEXT,
    street  TEXT,
    number  INT,
    city    TEXT
);

CREATE TABLE IF NOT EXISTS orders
(
    id          INT PRIMARY KEY,
    customer_id INT,
    name        TEXT,
    surname     TEXT,
    street      TEXT,
    number      INT,
    city        TEXT
);

CREATE TABLE IF NOT EXISTS order_product
(
    order_id      INT,
    customer_id   INT,
    name          TEXT,
    surname       TEXT,
    street        TEXT,
    number        INT,
    city          TEXT,
    product_id    INT,
    product_name  TEXT,
    price         INT,
    category_id   INT,
    category_name TEXT,
    count         INT,
    PRIMARY KEY ((order_id), product_id)
);

CREATE TABLE IF NOT EXISTS order_product_by_customer
(
    order_id      INT,
    customer_id   INT,
    name          TEXT,
    surname       TEXT,
    street        TEXT,
    number        INT,
    city          TEXT,
    product_id    INT,
    product_name  TEXT,
    price         INT,
    category_id   INT,
    category_name TEXT,
    count         INT,
    PRIMARY KEY ((customer_id), product_id, order_id)
);

CREATE TABLE IF NOT EXISTS product_count_by_category_and_customer
(
    customer_id INT,
    name TEXT,
    surname TEXT,
    city TEXT,
    street TEXT,
    number INT,
    category_id INT,
    category_name TEXT,
    product_count INT,
    PRIMARY KEY ((customer_id, category_id), product_count)
) WITH CLUSTERING ORDER BY (product_count DESC);