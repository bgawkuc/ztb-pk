from random import randint, seed

import os
import csv

seed(123)

PRODUCTS_NUMBER = 20
CUSTOMERS_NUMBER = 300
ORDERS_NUMBER = 2000
NEW_POSITIONS = 10000
NEW_ORDERS = NEW_POSITIONS // PRODUCTS_NUMBER


def get_file_path(file_name):
    return os.path.join('mongo', 'data-files', file_name) if 'mongo' in file_name else os.path.join('data-files',
                                                                                                    file_name)


def generate_large_order_data(file_name='large_order.csv'):
    with open(get_file_path(file_name), 'w', newline='') as csvfile:
        fieldnames = ['id', 'customer_id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Generate one large order with 10,000 positions for a random customer
        large_order_customer_id = randint(1, CUSTOMERS_NUMBER - 1)
        for i in range(1, NEW_ORDERS + 1):
            writer.writerow({'id': ORDERS_NUMBER + i, 'customer_id': large_order_customer_id})


def generate_large_order_product_data(file_name='large_order_product.csv'):
    with open(get_file_path(file_name), 'w', newline='') as csvfile:
        fieldnames = ['order_id', 'product_id', 'count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Generate 10,000 positions for the large order
        for i in range(1, NEW_ORDERS + 1):
            for product_id in range(1, PRODUCTS_NUMBER + 1):
                count = randint(1, 10)
                writer.writerow({'order_id': ORDERS_NUMBER + i, 'product_id': product_id, 'count': count})


if __name__ == "__main__":
    generate_large_order_data()
    generate_large_order_product_data()
    print("Large order CSV files generated successfully.")
