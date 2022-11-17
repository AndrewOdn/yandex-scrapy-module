# -*- coding: utf-8 -*-
from sqlalchemy import Column, MetaData, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.functions import now
from sqlalchemy.sql.sqltypes import BIGINT, TEXT, VARCHAR, DateTime

Base = declarative_base(metadata=MetaData(schema="sbermarket"))
"""Модели Таблиц в бд"""


class skus(Base):  # type: ignore
    __tablename__ = "skus"
    barcode = Column(VARCHAR(50), primary_key=True)
    sber_sku = Column(BIGINT)
    yandex_sku = Column(BIGINT)
    ozon_sku = Column(BIGINT)


class Image(Base):  # type: ignore
    __tablename__ = "image"
    product_id = Column(BIGINT, primary_key=True)
    img = Column(TEXT, nullable=True)


class Category(Base):  # type: ignore
    __tablename__ = "category"
    product_id = Column(BIGINT, primary_key=True)
    category_master = Column(VARCHAR(256), nullable=True)
    category_web = Column(VARCHAR(256), nullable=True, default=None)


class Product(Base):  # type: ignore
    __tablename__ = "product"
    product_id = Column(BIGINT, primary_key=True)
    brand = Column(VARCHAR(128), nullable=True)
    barcodes = Column(TEXT, nullable=True, default=None)
    price = Column(BIGINT, nullable=True, default=None)
    price_second = Column(BIGINT, nullable=True, default=None)
    model = Column(TEXT, nullable=True, default=None)
    article = Column(VARCHAR(128), nullable=True, default=None)
    name = Column(TEXT, nullable=True, default=None)
    url = Column(VARCHAR(256), nullable=True, default=None)
    category = Column(TEXT, nullable=True, default=None)
    updated = Column(DateTime, nullable=True, default=now())
    """Название товара"""


class Attributes(Base):  # type: ignore
    __tablename__ = "attributes"
    product_id = Column(BIGINT, primary_key=True)

    parameters = Column(TEXT)


class Sber(Base):  # type: ignore
    __tablename__ = "sber"
    __table_args__ = (PrimaryKeyConstraint("sku_id", "time"),)
    sku_id = Column(BIGINT, primary_key=True)
    price = Column(BIGINT, nullable=True, default=None)
    time = Column(BIGINT, primary_key=True)


class prices(Base):  # type: ignore
    __tablename__ = "prices"
    name = Column(TEXT, nullable=True, default=None)
    yandex_price = Column(BIGINT, nullable=True, default=None)
    ozon_price = Column(BIGINT, nullable=True, default=None)
    sber_price = Column(BIGINT, nullable=True, default=None)
    yandex_link = Column(TEXT, nullable=True, default=None)
    ozon_link = Column(VARCHAR(256), nullable=True, default=None)
    sber_link = Column(VARCHAR(256), nullable=True, default=None)
    review = Column(BIGINT, nullable=True, default=None)
    offers_count = Column(BIGINT, nullable=True, default=None)
    interested = Column(BIGINT, nullable=True, default=None)
    barcode = Column(VARCHAR(50), primary_key=True)
    yandex_level = Column(BIGINT, nullable=True, default=None)
    ozon_level = Column(BIGINT, nullable=True, default=None)
    sber_level = Column(BIGINT, nullable=True, default=None)
