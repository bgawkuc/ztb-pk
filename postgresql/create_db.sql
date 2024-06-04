CREATE TABLE IF NOT EXISTS categories
(
    id            SERIAL PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS products
(
    id           SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    price        INT          NOT NULL,
    category_id  INT,
    FOREIGN KEY (category_id) REFERENCES categories (id)
);

CREATE TABLE IF NOT EXISTS customers
(
    id      SERIAL PRIMARY KEY,
    name    VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    street  VARCHAR(255) NOT NULL,
    number  INT          NOT NULL,
    city    VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS orders
(
    id          SERIAL PRIMARY KEY,
    customer_id INT,
    FOREIGN KEY (customer_id) REFERENCES customers (id)
);

CREATE TABLE IF NOT EXISTS order_product
(
    order_id   INT,
    product_id INT,
    count      INT,
    FOREIGN KEY (order_id) REFERENCES orders (id),
    FOREIGN KEY (product_id) REFERENCES products (id)
);