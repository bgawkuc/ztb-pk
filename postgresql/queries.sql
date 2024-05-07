--  for all customer (id=1) orders finds the names of the products
SELECT o.id AS order_id, p.product_name
FROM orders o
         JOIN order_product od ON o.id = od.order_id
         JOIN products p ON od.product_id = p.id
WHERE o.customer_id = 1;

--  for an order (id=2) finds all products with category, price and quantity
SELECT p.product_name, c.category_name, p.price, od.count AS quantity
FROM order_product od
         JOIN products p ON od.product_id = p.id
         JOIN categories c ON p.category_id = c.id
WHERE od.order_id = 2;

--  finds order (id=2) total value, write all order products with price, count and product total
SELECT o.id               AS order_id,
       p.product_name,
       p.price,
       od.count           AS quantity,
       p.price * od.count AS product_total,
       (SELECT SUM(p.price * od.count)
        FROM orders o
                 JOIN order_product od ON o.id = od.order_id
                 JOIN products p ON od.product_id = p.id
        WHERE o.id = 2)   AS total_order_value
FROM orders o
         JOIN
     order_product od ON o.id = od.order_id
         JOIN
     products p ON od.product_id = p.id
WHERE o.id = 2;

--  finds customer (id=1) address and number of orders
SELECT CONCAT(c.street, ', ', c.number, ', ', c.city) AS address,
       COUNT(o.id)                                    AS number_of_orders
FROM customers c
         LEFT JOIN
     orders o ON c.id = o.customer_id
WHERE c.id = 1
GROUP BY c.id;

--  finds number of orders containing products from each category
SELECT c.category_name, COALESCE(COUNT(DISTINCT op.order_id), 0) AS number_of_orders
FROM order_product op
         RIGHT JOIN products p ON p.id = op.product_id
         JOIN categories c ON c.id = p.category_id
GROUP BY c.id;

-- finds customer with the most ordered products from given category (id=1)
SELECT c.id,
       c.name,
       c.surname,
       CONCAT(c.street, ', ', c.number, ', ', c.city) AS address,
       SUM(op.count)                                  AS count
FROM customers c
         JOIN orders o ON c.id = o.customer_id
         JOIN order_product op ON o.id = op.order_id
         JOIN products p ON p.id = op.product_id
         JOIN categories cat ON cat.id = p.category_id
WHERE cat.id = 1
GROUP BY c.id
ORDER BY count DESC
LIMIT 1;

--  finds all distinct products ordered by given customer (id=1) with number of orders and total count
SELECT DISTINCT p.product_name, COUNT(o.id), SUM(op.count)
FROM products p
         JOIN order_product op ON p.id = op.product_id
         JOIN orders o ON o.id = op.order_id
         JOIN customers c ON c.id = o.customer_id
WHERE c.id = 1
GROUP BY p.id;

--  finds customer that has spent the most on products from given category (id=1)
SELECT c.id,
       c.name,
       c.surname,
       CONCAT(c.street, ', ', c.number, ', ', c.city) AS address,
       SUM(op.count * p.price)                        AS total_value
FROM customers c
         JOIN orders o ON c.id = o.customer_id
         JOIN order_product op ON o.id = op.order_id
         JOIN products p ON p.id = op.product_id
         JOIN categories cat ON cat.id = p.category_id
WHERE cat.id = 1
GROUP BY c.id
ORDER BY total_value DESC
LIMIT 1;

--  delete all given client's (id=1) orders with products
BEGIN;
DELETE
FROM order_product op
WHERE op.order_id IN (SELECT o.id FROM orders o WHERE o.customer_id = 1);

DELETE
FROM orders o
WHERE o.customer_id = 1;
COMMIT;

--  batch delete 1000 rows from order_product table
BEGIN;
WITH cte AS (SELECT order_id, product_id FROM order_product LIMIT 1000)
DELETE
FROM order_product op USING cte
WHERE op.order_id = cte.order_id
  AND op.product_id = cte.product_id;
COMMIT;

--  delete all entries for product with given id (id=1) from order_product table
BEGIN;
DELETE
FROM order_product op
WHERE op.product_id = 1;
COMMIT;

--  insert big order from CSV file
BEGIN;
