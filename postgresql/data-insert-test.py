import psycopg2
import os
import csv


def get_file_path(file_name):
    return os.path.join('../data-files', file_name)


def insert_large_data(large_order_filename='large_order.csv', large_order_product_filename='large_order_product.csv'):
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
            print(row)
            order_product_insert_command += f' ({row["order_id"]}, {row["product_id"]}, {row["count"]}),'
        order_product_insert_command = order_product_insert_command.removesuffix(',')

    print(order_insert_command)
    print('----------------------------------')
    print(order_product_insert_command)

    try:
        with psycopg2.connect(host='localhost', database='grocery_store', user='postgres', password='postgres') as conn:
            with conn.cursor() as cur:
                cur.execute(order_insert_command)
                cur.execute(order_product_insert_command)
                conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        if conn:
            conn.rollback()
        print(error)


if __name__ == '__main__':
    insert_large_data()
