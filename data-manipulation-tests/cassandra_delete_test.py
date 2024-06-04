import os
import csv


def get_file_path(file_name):
    return os.path.join('../data-files', file_name)


def generate_delete_queries(order_product_delete_file='order_product_delete_cassandra.csv',
                            product_count_update_file_name='product_count_cassandra_delete_update.csv',
                            result_file='cassandra_delete_script.txt'):
    with open(result_file, 'w') as result_file:
        with open(get_file_path(order_product_delete_file), 'r') as delete_file:
            reader = csv.DictReader(delete_file)
            for row in reader:
                delete_command_1 = f'''DELETE FROM order_product
WHERE order_id = {row['order_id']} AND product_id = {row['product_id']};'''

                delete_command_2 = f'''DELETE FROM order_product_by_customer
WHERE order_id = {row['order_id']} AND product_id = {row['product_id']} AND customer_id = {row['customer_id']};'''

                result_file.write(delete_command_1 + '\n')
                result_file.write(delete_command_2 + '\n')

        with open(get_file_path(product_count_update_file_name), 'r') as order_file:
            reader = csv.DictReader(order_file)
            for row in reader:
                update_command = f'''UPDATE product_count_by_category_and_customer
SET product_count = {row['product_count']}
WHERE category_id = {row['category_id']} AND customer_id = {row['customer_id']};'''

                result_file.write(update_command + '\n')


if __name__ == '__main__':
    generate_delete_queries()
