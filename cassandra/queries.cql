USE grocery_store;

SELECT order_id, product_name
FROM order_product_by_customer
WHERE customer_id = 1;

SELECT product_name, price, count
FROM order_product
WHERE order_id = 2;

SELECT order_id, product_name, price, count, price * count AS product_total
FROM order_product
WHERE order_id = 2
GROUP BY order_id, product_id;

SELECT street + ', ' + cast(number AS TEXT) + ', ' + city AS address, count(*) AS orders_number
FROM order_product_by_customer
WHERE customer_id = 1
GROUP BY customer_id;

SELECT product_name, count(*) AS number_of_orders, sum(count) AS total_count
FROM order_product_by_customer
WHERE customer_id = 1
GROUP BY product_id;

SELECT customer_id, name, surname, street + ', ' + cast(number AS TEXT) + ', ' + city AS address, product_count
FROM product_count_by_category_and_customer
WHERE category_id = 1
ORDER BY product_count DESC
LIMIT 1;