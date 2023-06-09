from werkzeug.security import generate_password_hash
import csv
from faker import Faker
import random

num_users = 100
num_products = 2000
num_purchases = 2500
num_reviews = 1000

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')


def gen_users(num_users):
    with open('Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            email = profile['mail']
            plain_password = f'pass{uid}'
            password = generate_password_hash(plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            seller = fake.random.choice([True, False])
            balance = fake.pyfloat(positive=True)
            address = fake.sentence(nb_words=4)[:-1]
            writer.writerow([uid, email, password, firstname, lastname, seller, balance, address])
        print(f'{num_users} generated')
    return


def gen_products(num_products):
    available_pids = []
    available_categories = ['Apps', 'Food', 'Books', 'Electronics', 'Health', 'Outdoor', 'Entertainment']
    with open('Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        for pid in range(num_products):
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)
            name = fake.sentence(nb_words=4)[:-1]
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            category_index = random.randint(0, len(available_categories) - 1)
            category = available_categories[category_index]
            description = fake.sentence(nb_words=50)[:-1]
            available = fake.pybool()
            image = fake.image_url()
            if available:
                available_pids.append(pid)
            writer.writerow([pid, name, category, description, price, available, image])
        print(f'{num_products} generated; {len(available_pids)} available')
    return available_pids


def gen_purchases(num_purchases, available_pids):
    with open('Purchases.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        for id in range(num_purchases):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            sid = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_element(elements=available_pids)
            quantity = fake.random_int(min=1)
            time_purchased = fake.date_time()
            fulfillment_status = "Not Fulfilled"
            writer.writerow([id, uid, sid, pid, quantity, time_purchased, fulfillment_status])
        print(f'{num_purchases} generated')
    return

def gen_reviews(num_reviews, available_pids):
    with open('Feedback.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Reviews...', end=' ', flush=True)
        for id in range(num_reviews):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_element(elements=available_pids)
            sid = fake.random_int(min=0, max=num_users-1)
            time_submitted = fake.date_time()
            review = fake.sentence()
            rating = fake.random_int(min=1, max=5)
            upvotes = fake.random_int()
            image = fake.image_url()
            writer.writerow([id, uid, pid, sid, time_submitted, review, rating, upvotes, image])
        print(f'{num_reviews} generated')
    return

def gen_carts(num_users, available_pids):
    with open('Carts.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Carts...', end=' ', flush=True)
        for id in range(num_users):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_element(elements=available_pids)
            quantity = fake.random_int(min=1)
            unit_price = fake.pyfloat(positive=True)
            sid = -1
            saved = False
            writer.writerow([uid, pid, quantity, unit_price, sid, saved])
        print(f'{num_users} generated')
    return

def gen_sellers(available_pids):
    sellers = []
    with open('Users.csv','r') as f:
        reader = csv.reader(f,delimiter = ',')
        for row in reader:
            if row[-3] == 'True':
                sellers.append(row[0])

    with open('Sellers.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Inventories...', end=' ', flush=True)
        for sid in sellers:
            sid = int(sid)
            pids = []
            if sid % 10 == 0:
                print(f'{sid}', end=' ', flush=True)
            for i in range(fake.random_int(min=20,max=100)):
                pid = fake.random_element(elements=available_pids)
                if pid in pids: 
                    continue
                pids.append(pid)
                quantity = fake.random_int(min=1,max=100)
                unit_price = fake.pyfloat(positive=True,max_value=1000,right_digits=2)
                writer.writerow([sid, pid, quantity, unit_price])
        print(f'{len(sellers)} generated')
    return


gen_users(num_users)
available_pids = gen_products(num_products)
gen_purchases(num_purchases, available_pids)
gen_reviews(num_reviews, available_pids)
gen_carts(num_users, available_pids)
gen_sellers(available_pids)
