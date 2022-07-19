import sqlalchemy as sq

from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric

Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publisher'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=40), unique=True, nullable=False)

    def __repr__(self):
        return f'Publisher {self.id}: {self.name}'


class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    title = Column(String(length=40), nullable=False)
    id_publisher = Column(Integer, ForeignKey('publisher.id'), nullable=False)

    publisher = relationship(Publisher, backref='book')

    def __repr__(self):
        return f'Book {self.id}: {self.title}: {self.id_publisher}'


class Shop(Base):
    __tablename__ = 'shop'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=40), nullable=False)

    def __repr__(self):
        return f'Shop {self.id}: {self.name}'


class Stock(Base):
    __tablename__ = 'stock'

    id = Column(Integer, primary_key=True)
    id_book = Column(Integer, ForeignKey('book.id'), nullable=False)
    id_shop = Column(Integer, ForeignKey('shop.id'), nullable=False)
    count = Column(Integer, nullable=False)

    book = relationship(Book, backref='stock')
    shop = relationship(Shop, backref='stock')

    def __repr__(self):
        return f'Stock {self.id}: {self.id_book}: {self.count}: {self.id_shop}'


class Sale(Base):
    __tablename__ = 'sale'

    id = Column(Integer, primary_key=True)
    price = Column(Numeric(precision=40, scale=2), nullable=False)
    date_sale = Column(DateTime, nullable=False)
    id_stock = Column(Integer, ForeignKey('stock.id'), nullable=False)
    count = Column(Integer, nullable=False)

    stock = relationship(Stock, backref='sale')

    def __repr__(self):
        return f'Sale {self.id}: {self.id_stock}: {self.price}: {self.date_sale}: {self.count}'


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
