from random import randint, seed

import faker
import csv
import os
import sys

seed(123)

categories = [
    'dairy', 'grains', 'condiments', 'snacks', 'frozen', 'produce', 'meat', 'seafood', 'legumes', 'canned', 'breads',
    'nuts_seeds', 'grains'
]

product_category_mapping = {
    'bread': 'breads', 'milk': 'dairy', 'eggs': 'dairy', 'butter': 'dairy', 'cheese': 'dairy', 'yogurt': 'dairy',
    'rice': 'grains', 'pasta': 'grains', 'flour': 'grains', 'sugar': 'condiments', 'salt': 'condiments', 'pepper': 'condiments',
    'oil': 'condiments', 'vinegar': 'condiments', 'ketchup': 'condiments', 'mustard': 'condiments', 'mayonnaise': 'condiments',
    'jam': 'condiments', 'honey': 'condiments', 'syrup': 'condiments', 'cereal': 'snacks', 'coffee': 'snacks', 'tea': 'snacks',
    'juice': 'snacks', 'water': 'snacks', 'soda': 'snacks', 'chips': 'snacks', 'crackers': 'snacks', 'cookies': 'snacks',
    'chocolate': 'snacks', 'ice cream': 'frozen', 'frozen vegetables': 'frozen', 'frozen fruits': 'frozen', 'frozen pizza': 'frozen',
    'frozen meals': 'frozen', 'fresh fruits': 'produce', 'fresh vegetables': 'produce', 'chicken': 'meat', 'beef': 'meat',
    'pork': 'meat', 'fish': 'seafood', 'shrimp': 'seafood', 'tofu': 'legumes', 'beans': 'legumes', 'soup': 'canned',
    'canned vegetables': 'canned', 'canned fruits': 'canned', 'canned beans': 'canned', 'canned soup': 'canned', 'canned tuna': 'canned',
    'bread rolls': 'breads', 'buns': 'breads', 'bagels': 'breads', 'tortillas': 'breads', 'pita bread': 'breads', 'croissants': 'breads',
    'lettuce': 'produce', 'tomatoes': 'produce', 'potatoes': 'produce', 'onions': 'produce', 'carrots': 'produce', 'bell peppers': 'produce',
    'spinach': 'produce', 'cucumbers': 'produce', 'avocados': 'produce', 'bananas': 'produce', 'apples': 'produce', 'oranges': 'produce',
    'grapes': 'produce', 'strawberries': 'produce', 'blueberries': 'produce', 'lemons': 'produce', 'limes': 'produce', 'peaches': 'produce',
    'pears': 'produce', 'kiwis': 'produce', 'mangoes': 'produce', 'pineapples': 'produce', 'watermelons': 'produce', 'cherries': 'produce',
    'dates': 'produce', 'figs': 'produce', 'plums': 'produce', 'raspberries': 'produce', 'blackberries': 'produce', 'cranberries': 'produce',
    'almonds': 'nuts_seeds', 'walnuts': 'nuts_seeds', 'pecans': 'nuts_seeds', 'cashews': 'nuts_seeds', 'peanuts': 'nuts_seeds',
    'sunflower seeds': 'nuts_seeds', 'pumpkin seeds': 'nuts_seeds', 'flaxseeds': 'nuts_seeds', 'chia seeds': 'nuts_seeds',
    'quinoa': 'grains', 'oats': 'grains', 'barley': 'grains', 'millet': 'grains', 'brown rice': 'grains', 'white rice': 'grains',
    'whole wheat bread': 'breads', 'whole wheat pasta': 'grains', 'corn tortillas': 'breads'
}

PRODUCTS_NUMBER = len(product_category_mapping)
CUSTOMERS_NUMBER = 300
ORDERS_NUMBER = int(sys.argv[1])


# mongo id field -> _id
def get_id_field_name(file_name):
    return '_id' if 'mongo' in file_name else 'id'


def get_file_path(file_name):
    return os.path.join('../mongo', 'data-files', file_name) if 'mongo' in file_name else os.path.join('../data-files', file_name)


def generate_categories_data(file_name='categories.csv'):
    with open(get_file_path(file_name), 'w', newline='') as csvfile:
        id_field = get_id_field_name(file_name)
        fieldnames = [id_field, 'category_name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for category_id, category in enumerate(categories):
            writer.writerow({id_field: category_id+1, 'category_name': category})


def generate_products_data(file_name='products.csv'):
    with open(get_file_path(file_name), 'w', newline='') as csvfile:
        id_field = get_id_field_name(file_name)
        fieldnames = [id_field, 'product_name', 'price', 'category_id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for product_id, (product, category) in enumerate(product_category_mapping.items()):
            price = randint(3, 35)
            category_id = categories.index(category)
            writer.writerow({id_field: product_id+1, 'product_name': product, 'price': price, 'category_id': category_id+1})


def generate_customers_data(file_name='customers.csv'):
    fake = faker.Faker()

    with open(get_file_path(file_name), 'w', newline='') as csvfile:
        id_field = get_id_field_name(file_name)
        fieldnames = [id_field, 'name', 'surname', 'street', 'number', 'city']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for client_id in range(CUSTOMERS_NUMBER):
            name = fake.first_name()
            surname = fake.last_name()
            street = fake.street_name()
            number = fake.building_number()
            city = fake.city()

            writer.writerow({id_field: client_id+1, 'name': name, 'surname': surname, 'street': street, 'number': number,
                             'city': city})


def generate_orders_data(file_name='orders.csv'):
    with open(get_file_path(file_name), 'w', newline='') as csvfile:
        id_field = get_id_field_name(file_name)
        fieldnames = [id_field, 'customer_id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for order_id in range(ORDERS_NUMBER):
            customer_id = randint(1, CUSTOMERS_NUMBER - 1)
            writer.writerow({id_field: order_id+1, 'customer_id': customer_id})


def generate_order_product_data(file_name='order_product.csv'):
    with open(get_file_path(file_name), 'w', newline='') as csvfile:
        fieldnames = ['order_id', 'product_id', 'count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for order_id in range(ORDERS_NUMBER):
            products_number = randint(1, 20)
            unique_product_ids = []
            for _ in range(products_number):
                while True:
                    product_id = randint(1, PRODUCTS_NUMBER)
                    if product_id not in unique_product_ids:
                        unique_product_ids.append(product_id)
                        break
                count = randint(1, 10)
                writer.writerow({'order_id': order_id+1, 'product_id': product_id, 'count': count})


if __name__ == "__main__":
    generate_categories_data()
    generate_categories_data('categories_mongo.csv')

    generate_products_data()
    generate_products_data('products_mongo.csv')

    generate_customers_data()
    generate_customers_data('customers_mongo.csv')

    generate_orders_data()
    generate_orders_data('orders_mongo.csv')

    generate_order_product_data()
    generate_order_product_data('order_product_mongo.csv')
