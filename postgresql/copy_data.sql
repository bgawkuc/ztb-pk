COPY categories (id, category_name)
    FROM '/tmp/categories.csv' DELIMITER ',' CSV HEADER;

COPY customers (id, name, surname, street, number, city)
    FROM '/tmp/customers.csv' DELIMITER ',' CSV HEADER;

COPY products (id, product_name, price, category_id)
    FROM '/tmp/products.csv' DELIMITER ',' CSV HEADER;

COPY orders (id, customer_id)
    FROM '/tmp/orders.csv' DELIMITER ',' CSV HEADER;

COPY order_product (order_id, product_id, count)
    FROM '/tmp/order_product.csv' DELIMITER ',' CSV HEADER;