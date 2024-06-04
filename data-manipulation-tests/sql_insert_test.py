import os
import csv


def get_file_path(file_name):
    return os.path.join('../data-files', file_name)


def generate_insert(large_order_filename='orders_insert.csv', large_order_product_filename='order_product_insert.csv'):
    order_insert_command = '''
    INSERT INTO orders (id, customer_id)
    VALUES
    '''

    with open(get_file_path(large_order_filename), 'r') as order_file:
        reader = csv.DictReader(order_file)
        for row in reader:
            order_insert_command += f' ({row["id"]}, {row["customer_id"]}),'
        order_insert_command = order_insert_command.removesuffix(',')

    order_product_insert_command = '''
    INSERT INTO order_product (order_id, product_id, count)
    VALUES
    '''

    with open(get_file_path(large_order_product_filename), 'r') as order_product_file:
        reader = csv.DictReader(order_product_file)
        for row in reader:
            order_product_insert_command += f' ({row["order_id"]}, {row["product_id"]}, {row["count"]}),'
        order_product_insert_command = order_product_insert_command.removesuffix(',')

    print(order_insert_command)
    print('----------------------------------')
    print(order_product_insert_command)


if __name__ == '__main__':
    generate_insert()
