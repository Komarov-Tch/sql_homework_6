import sqlalchemy
import json
import os
from sqlalchemy.orm import sessionmaker
from models import *

rec = []


def write_publisher(pk, fields):
    publisher = Publisher(id=pk, **fields)
    rec.append(publisher)


def write_book(pk, fields):
    book = Book(id=pk, **fields)
    rec.append(book)


def write_shop(pk, fields):
    shop = Shop(id=pk, **fields)
    rec.append(shop)


def write_stock(pk, fields):
    stock = Stock(id=pk, **fields)
    rec.append(stock)


def write_sale(pk, fields):
    sale = Sale(id=pk, **fields)
    rec.append(sale)


def writedb(model, pk, fields):
    if model == 'publisher':
        write_publisher(pk, fields)
    elif model == 'book':
        write_book(pk, fields)
    elif model == 'shop':
        write_shop(pk, fields)
    elif model == 'stock':
        write_stock(pk, fields)
    elif model == 'sale':
        write_sale(pk, fields)


print('Введите пользователя: ')
user = input()
print('Введите пароль: ')
password = input()
print('Введите название базы данных: ')
db_name = input()
DSN = 'postgresql://' + user + ':' + password + '@localhost:5432/' + db_name
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)
Session = sessionmaker(bind=engine)
session = Session()

jsonData = os.path.join(os.getcwd(), 'data.json')
f = open(jsonData, encoding='utf-8')
dictData = json.load(f)
for dic in dictData:
    writedb(model=dic['model'], pk=dic['pk'], fields=dic['fields'])
session.add_all(rec)
session.commit()
session.close()

print('Введите издательство:')
id_publisher = input()
if id_publisher.isdigit():
    id_publisher = int(id_publisher)
    for c in session.query(Publisher).filter(Publisher.id == id_publisher).all():
        print(c)
else:
    for c in session.query(Publisher).filter(Publisher.name == id_publisher).all():
        print(c)
