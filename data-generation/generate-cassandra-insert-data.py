from random import randint, seed

import os
import csv
import sys

seed(123)

PRODUCTS_NUMBER = 20
CUSTOMERS_NUMBER = 300
ORDERS_NUMBER = int(sys.argv[1])
NEW_POSITIONS = int(sys.argv[2])
NEW_ORDERS = NEW_POSITIONS // PRODUCTS_NUMBER


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


def generate_order_insert_data(customer_data, large_order_customer_id, file_name='orders_insert_cassandra.csv'):
    with open(get_file_path(file_name), 'w', newline='') as csvfile:
        fieldnames = ['id', 'customer_id', 'name', 'surname', 'street', 'number', 'city']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        name = customer_data[str(large_order_customer_id)]['name']
        surname = customer_data[str(large_order_customer_id)]['surname']
        street = customer_data[str(large_order_customer_id)]['street']
        number = customer_data[str(large_order_customer_id)]['number']
        city = customer_data[str(large_order_customer_id)]['city']
        for i in range(1, NEW_ORDERS + 1):
            writer.writerow(
                {'id': ORDERS_NUMBER + i, 'customer_id': large_order_customer_id, 'name': name, 'surname': surname,
                 'street': street, 'number': number, 'city': city})


def generate_order_product_insert_data(product_data, customer_data, category_data, customer_id,
                                       file_name_1='order_product_insert_cassandra.csv',
                                       file_name_2='product_count_by_category_and_customer_update_cassandra.csv'):
    name = customer_data[str(customer_id)]['name']
    surname = customer_data[str(customer_id)]['surname']
    street = customer_data[str(customer_id)]['street']
    number = customer_data[str(customer_id)]['number']
    city = customer_data[str(customer_id)]['city']
    changes_dict = {}
    with open(get_file_path(file_name_1), 'w', newline='') as csvfile:
        fieldnames = ['order_id', 'customer_id', 'name', 'surname', 'street', 'number', 'city', 'product_id',
                      'product_name', 'price', 'category_id', 'category_name', 'count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(1, NEW_ORDERS + 1):
            for product_id in range(1, PRODUCTS_NUMBER + 1):
                count = randint(1, 10)
                product_name = product_data[str(product_id)]['product_name']
                price = product_data[str(product_id)]['price']
                category_id = product_data[str(product_id)]['category_id']
                category_name = product_data[str(product_id)]['category_name']
                writer.writerow({'order_id': ORDERS_NUMBER + i, 'customer_id': customer_id, 'name': name,
                                 'surname': surname, 'street': street, 'number': number, 'city': city,
                                 'product_id': product_id, 'product_name': product_name, 'price': price,
                                 'category_id': category_id, 'category_name': category_name, 'count': count})
                if category_id not in changes_dict.keys():
                    changes_dict[category_id] = 0
                changes_dict[category_id] += count

    product_count_data = read_product_count_data()
    with open(get_file_path(file_name_2), 'w', newline='') as csvfile:
        fieldnames = ['category_id', 'category_name', 'customer_id', 'name', 'surname', 'street', 'number', 'city',
                      'product_count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for category_id, count in changes_dict.items():
            category_name = category_data[category_id]['category_name']
            old_count = int(product_count_data[str(customer_id)][str(category_id)]['product_count'])
            writer.writerow(
                {'category_id': category_id, 'category_name': category_name, 'customer_id': customer_id,
                 'name': name, 'surname': surname, 'street': street, 'number': number, 'city': city,
                 'product_count': old_count + count})


if __name__ == "__main__":
    customer_id = randint(1, CUSTOMERS_NUMBER - 1)
    customer_data = read_customer_data()
    product_data = read_product_data()
    category_data = read_category_data()
    generate_order_insert_data(customer_data, customer_id)
    generate_order_product_insert_data(product_data, customer_data, category_data, customer_id)
