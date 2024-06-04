import random
from random import randint, seed

import os
import csv
import sys

seed(123)

PRODUCTS_NUMBER = 20
CUSTOMERS_NUMBER = 300
ORDERS_NUMBER = int(sys.argv[1])
TO_DELETE = int(sys.argv[2])


def get_file_path(file_name):
    return os.path.join('../data-files', file_name)


def read_customer_data(file_name='customers.csv'):
    customer_dict = {}
    with open(get_file_path(file_name), 'r') as customers_file:
        reader = csv.DictReader(customers_file)
        for row in reader:
            customer_dict[row['id']] = row
    return customer_dict


def read_category_data(file_name='categories.csv'):
    category_dict = {}
    with open(get_file_path(file_name), 'r') as customers_file:
        reader = csv.DictReader(customers_file)
        for row in reader:
            category_dict[row['id']] = row
    return category_dict


def read_product_count_data(file_name='product_count_by_category_and_customer_cassandra.csv'):
    product_count_dict = {}
    with open(get_file_path(file_name), 'r') as customers_file:
        reader = csv.DictReader(customers_file)
        for row in reader:
            customer_id = row['customer_id']
            category_id = row['category_id']
            if customer_id not in product_count_dict.keys():
                product_count_dict[customer_id] = {}
            product_count_dict[customer_id][category_id] = row
    return product_count_dict


def read_product_data(file_name='products_cassandra.csv'):
    product_dict = {}
    with open(get_file_path(file_name), 'r') as customers_file:
        reader = csv.DictReader(customers_file)
        for row in reader:
            product_dict[row['id']] = row
    return product_dict


def read_order_product_data(file_name='order_product_cassandra.csv'):
    with open(get_file_path(file_name), 'r') as order_product_file:
        reader = csv.DictReader(order_product_file)
        return list(reader)


def generate_delete_data(file_name_1='order_product_delete_cassandra.csv',
                         file_name_2='product_count_cassandra_delete_update.csv'):
    order_product_data = read_order_product_data()
    product_data = read_product_data()
    product_count_data = read_product_count_data()
    changes_dict = {}
    with open(get_file_path(file_name_1), 'w') as delete_data_file:
        rows_to_delete = random.sample(range(len(order_product_data)), TO_DELETE)
        fieldnames = ['customer_id', 'order_id', 'product_id']
        writer = csv.DictWriter(delete_data_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows_to_delete:
            customer_id = order_product_data[row]['customer_id']
            product_id = order_product_data[row]['product_id']
            order_id = order_product_data[row]['order_id']
            category_id = product_data[product_id]['category_id']
            count = int(order_product_data[row]['count'])
            writer.writerow({'customer_id': customer_id, 'product_id': product_id, 'order_id': order_id})
            dict_key = category_id + '|' + customer_id
            if dict_key not in changes_dict.keys():
                changes_dict[dict_key] = 0
            changes_dict[dict_key] += count

    with open(get_file_path(file_name_2), 'w') as delete_update_file:
        fieldnames = ['category_id', 'customer_id', 'product_count']
        writer = csv.DictWriter(delete_update_file, fieldnames=fieldnames)
        writer.writeheader()
        for dict_key, count in changes_dict.items():
            category_id, customer_id = dict_key.split('|')
            old_count = int(product_count_data[customer_id][category_id]['product_count'])
            writer.writerow(
                {'category_id': category_id, 'customer_id': customer_id, 'product_count': old_count - count})


if __name__ == '__main__':
    generate_delete_data()
