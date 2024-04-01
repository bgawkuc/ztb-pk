USE grocery_store;

#  for all customer (id=1) orders finds the names of the products
SELECT o.id AS order_id, p.product_name
FROM orders o
JOIN order_product od ON o.id = od.order_id
JOIN products p ON od.product_id = p.id
WHERE o.customer_id = 1;

#  for an order (id=2) finds all products with category, price and quantity
SELECT p.product_name, c.category_name, p.price, od.count AS quantity
FROM order_product od
JOIN products p ON od.product_id = p.id
JOIN categories c ON p.category_id = c.id
WHERE od.order_id = 2;

# finds order (id=2) total value, write all order products with price, count and product total
SELECT
    o.id AS order_id,
    p.product_name,
    p.price,
    od.count AS quantity,
    p.price * od.count AS product_total,
    (SELECT SUM(p.price * od.count)
     FROM orders o
     JOIN order_product od ON o.id = od.order_id
     JOIN products p ON od.product_id = p.id
     WHERE o.id = 2) AS total_order_value
FROM
    orders o
JOIN
    order_product od ON o.id = od.order_id
JOIN
    products p ON od.product_id = p.id
WHERE
    o.id = 2;

# finds customer (id=1) address and number of orders
SELECT
    CONCAT(c.street, ', ', c.number, ', ', c.city) AS address,
    COUNT(o.id) AS number_of_orders
FROM
    customers c
LEFT JOIN
    orders o ON c.id = o.customer_id
WHERE
    c.id = 1;


