import csv
import os

def get_file_path(file_name):
    return os.path.join('data-files', file_name)


def generate_products_cassandra_data(file_name='products_cassandra.csv'):
    products_file_path = get_file_path('products.csv')
    categories_file_path = get_file_path('categories.csv')

    category_dict = {}
    with open(categories_file_path, 'r') as categories_file:
        reader = csv.DictReader(categories_file)
        for row in reader:
            category_dict[row['id']] = row['category_name']

    with open(get_file_path(file_name), 'w', newline='') as csvfile:
        fieldnames = ['id', 'product_name', 'price', 'category_id', 'category_name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        with open(products_file_path, 'r') as products_file:
            reader = csv.DictReader(products_file)
            for row in reader:
                writer.writerow({
                    'id': row['id'],
                    'product_name': row['product_name'],
                    'price': row['price'],
                    'category_id': row['category_id'],
                    'category_name': category_dict[row['category_id']]
                })

def generate_orders_cassandra_data(file_name='orders_cassandra.csv'):
    orders_file_path = get_file_path('orders.csv')
    customers_file_path = get_file_path('customers.csv')

    customer_dict = {}
    with open(customers_file_path, 'r') as customers_file:
        reader = csv.DictReader(customers_file)
        for row in reader:
            customer_dict[row['id']] = row

    with open(get_file_path(file_name), 'w', newline='') as csvfile:
        fieldnames = ['id', 'customer_id', 'name', 'surname', 'street', 'number', 'city']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        with open(orders_file_path, 'r') as orders_file:
            reader = csv.DictReader(orders_file)
            for row in reader:
                customer = customer_dict[row['customer_id']]
                writer.writerow({
                    'id': row['id'],
                    'customer_id': row['customer_id'],
                    'name': customer['name'],
                    'surname': customer['surname'],
                    'street': customer['street'],
                    'number': customer['number'],
                    'city': customer['city']
                })

def generate_order_product_cassandra_data(file_name='order_product_cassandra.csv'):
    order_product_file_path = get_file_path('order_product.csv')
    orders_file_path = get_file_path('orders.csv')
    customers_file_path = get_file_path('customers.csv')
    products_file_path = get_file_path('products.csv')
    categories_file_path = get_file_path('categories.csv')

    customer_dict = {}
    with open(customers_file_path, 'r') as customers_file:
        reader = csv.DictReader(customers_file)
        for row in reader:
            customer_dict[row['id']] = row

    product_dict = {}
    category_dict = {}
    order_dict = {}
    with open(products_file_path, 'r') as products_file:
        reader = csv.DictReader(products_file)
        for row in reader:
            product_dict[row['id']] = row

    with open(categories_file_path, 'r') as categories_file:
        reader = csv.DictReader(categories_file)
        for row in reader:
            category_dict[row['id']] = row['category_name']

    with open(orders_file_path, 'r') as orders_file:
        reader = csv.DictReader(orders_file)
        for row in reader:
            order_dict[row['id']] = row['customer_id']

    with open(get_file_path(file_name), 'w', newline='') as csvfile:
        fieldnames = ['order_id', 'customer_id', 'name', 'surname', 'street', 'number', 'city', 'product_id', 'product_name', 'price', 'category_id', 'category_name', 'count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        with open(order_product_file_path, 'r') as order_product_file:
            reader = csv.DictReader(order_product_file)
            for row in reader:
                customer = customer_dict[order_dict[row['order_id']]]
                product = product_dict[row['product_id']]
                writer.writerow({
                    'order_id': row['order_id'],
                    'customer_id': order_dict[row['order_id']],
                    'name': customer['name'],
                    'surname': customer['surname'],
                    'street': customer['street'],
                    'number': customer['number'],
                    'city': customer['city'],
                    'product_id': row['product_id'],
                    'product_name': product['product_name'],
                    'price': product['price'],
                    'category_id': product['category_id'],
                    'category_name': category_dict[product['category_id']],
                    'count': row['count']
                })

def generate_product_count_by_category_and_customer_cassandra_data(file_name="product_count_by_category_and_customer_cassandra.csv"):
    # Load data from previously generated CSV files
    with open(get_file_path('categories.csv'), 'r') as f:
        categories = list(csv.reader(f))
    with open(get_file_path('products.csv'), 'r') as f:
        products = list(csv.reader(f))
    with open(get_file_path('customers.csv'), 'r') as f:
        customers = list(csv.reader(f))
    with open(get_file_path('orders.csv'), 'r') as f:
        orders = list(csv.reader(f))
    with open(get_file_path('order_product.csv'), 'r') as f:
        order_products = list(csv.reader(f))

    # Create a dictionary mapping category IDs to names
    category_dict = {row[0]: row[1] for row in categories[1:]}

    # Create a dictionary mapping product IDs to their category ID and price
    product_dict = {row[0]: (row[3], row[2]) for row in products[1:]}

    # Create a dictionary mapping customer IDs to their details
    customer_dict = {row[0]: row[1:] for row in customers[1:]}

    # Create a dictionary mapping order IDs to their customer ID
    order_dict = {row[0]: row[1] for row in orders[1:]}

    # Create a dictionary to store total amount spent by each customer on each category
    result_dict = {customer_id: {category_id: 0 for category_id in category_dict.keys()} for customer_id in customer_dict.keys()}

    for row in order_products[1:]:
        order_id, product_id, count = row
        customer_id = order_dict[order_id]
        category_id, price = product_dict[product_id]

        # Update result_dict
        result_dict[customer_id][category_id] += int(count)

    # Write data to new CSV file
    with open(get_file_path(file_name), 'w', newline='') as csvfile:
        fieldnames = ['category_id', 'category_name', 'customer_id', 'name', 'surname', 'street', 'number', 'city', 'product_count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for customer_id, categories in result_dict.items():
            for category_id, product_count in categories.items():
                category_name = category_dict[category_id]
                name, surname, street, number, city = customer_dict[customer_id]
                writer.writerow({
                    'category_id': category_id,
                    'category_name': category_name,
                    'customer_id': customer_id,
                    'name': name,
                    'surname': surname,
                    'street': street,
                    'number': number,
                    'city': city,
                    'product_count': product_count
                })

if __name__ == "__main__":
    generate_products_cassandra_data()
    generate_orders_cassandra_data()
    generate_order_product_cassandra_data()
    generate_product_count_by_category_and_customer_cassandra_data()
    print("Cassandra CSV files generated successfully.")