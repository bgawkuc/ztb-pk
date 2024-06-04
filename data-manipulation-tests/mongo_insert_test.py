import os
import csv


def get_file_path(file_name):
    return os.path.join('../data-files', file_name)


def generate_insert(large_order_filename='orders_insert.csv', large_order_product_filename='order_product_insert.csv'):
    order_insert_command = '''
    db.orders.insert([
    '''

    with open(get_file_path(large_order_filename), 'r') as order_file:
        reader = csv.DictReader(order_file)
        for row in reader:
            order_insert_command += f' {{"_id": {row["id"]}, "customer_id": {row["customer_id"]}}},'
        order_insert_command = order_insert_command.removesuffix(',')
        order_insert_command += '])'

    order_product_insert_command = '''
    db.order_product.insert([
    '''

    with open(get_file_path(large_order_product_filename), 'r') as order_product_file:
        reader = csv.DictReader(order_product_file)
        for row in reader:
            order_product_insert_command += f' {{"order_id": {row["order_id"]}, "product_id": {row["product_id"]}, "count": {row["count"]}}},'
        order_product_insert_command = order_product_insert_command.removesuffix(',')
        order_product_insert_command += '])'

    print(order_insert_command)
    print('----------------------------------')
    print(order_product_insert_command)


if __name__ == '__main__':
    generate_insert()
