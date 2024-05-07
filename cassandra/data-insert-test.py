import os
import csv


def get_file_path(file_name):
    return os.path.join('../data-files', file_name)


def insert_large_data(large_order_file_name='large_order_cassandra.csv',
                      large_order_product_file_name='large_order_product_cassandra.csv',
                      product_count_update_file_name='product_count_by_category_and_customer_cassandra_update.csv'):
    order_insert_command = '''
    INSERT INTO orders (id, customer_id, name, surname, street, number, city)
    VALUES
    '''

    with open(get_file_path(large_order_file_name), 'r') as order_file:
        reader = csv.DictReader(order_file)
        for row in reader:
            order_insert_command += f' ({row["id"]}, {row["customer_id"]}, {row["name"]}, {row["surname"]}, {row["street"]}, {row["number"]}, {row["city"]}),'
        order_insert_command = order_insert_command.removesuffix(',')

    print(order_insert_command)
    print('----------------------------------')

    order_product_insert_command = '''
    INSERT INTO order_product (order_id, customer_id, name, surname, street, number, city, product_id, product_name, price, category_id, category_name, count)
    VALUES
    '''

    order_product_by_customer_insert_command = '''
    INSERT INTO order_product_by_customer (order_id, customer_id, name, surname, street, number, city, product_id, product_name, price, category_id, category_name, count)
    VALUES
    '''

    with open(get_file_path(large_order_product_file_name), 'r') as order_file:
        reader = csv.DictReader(order_file)
        for row in reader:
            order_product_insert_command += f' ({row["order_id"]}, {row["customer_id"]}, {row["name"]}, {row["surname"]}, {row["street"]}, {row["number"]}, {row["city"]}, {row["product_id"]}, {row["product_name"]}, {row["price"]}, {row["category_id"]}, {row["category_name"]}, {row["count"]}),'
            order_product_by_customer_insert_command += f' ({row["order_id"]}, {row["customer_id"]}, {row["name"]}, {row["surname"]}, {row["street"]}, {row["number"]}, {row["city"]}, {row["product_id"]}, {row["product_name"]}, {row["price"]}, {row["category_id"]}, {row["category_name"]}, {row["count"]}),'
        order_product_insert_command = order_insert_command.removesuffix(',')
        order_product_by_customer_insert_command = order_product_by_customer_insert_command.removesuffix(',')

    print(order_product_insert_command)
    print('----------------------------------')
    print(order_product_by_customer_insert_command)
    print('----------------------------------')

    with open(get_file_path(product_count_update_file_name), 'r') as order_file:
        reader = csv.DictReader(order_file)
        for row in reader:
            update_command = f'''
            UPDATE product_count_by_category_and_customer
            SET product_count = {row['product_count']}
            WHERE category_id = {row['category_id']} AND customer_id = {row['customer_id']}
            '''

            print(update_command)
            print('----------------------------------')


if __name__ == '__main__':
    insert_large_data()
