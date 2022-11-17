# -*- coding: utf-8 -*-
# mypy: ignore-errors
from sqlalchemy import Column, ForeignKey, Integer, PrimaryKeyConstraint
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import BIGINT, CHAR, DECIMAL, TEXT, VARCHAR, DateTime

Base = declarative_base()


class Marketplace(Base):
    __tablename__ = "marketplaces"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(VARCHAR(50), unique=True)
    fee = Column(Integer)
    extra_charge = Column(DECIMAL(10, 2))
    extra_charge_stone = Column(DECIMAL(10, 2))


class Organization(Base):
    __tablename__ = "organizations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(255))
    businesses = relationship("Business")


class Business(Base):
    __tablename__ = "businesses"
    __table_args__ = (PrimaryKeyConstraint("id", "marketplace_id"),)
    id = Column(Integer, primary_key=True)
    marketplace_id = Column(Integer, ForeignKey("marketplaces.id"), primary_key=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    name = Column(VARCHAR(255))
    email = Column(VARCHAR(255), nullable=True, default=None)
    password = Column(VARCHAR(255), nullable=True, default=None)
    token = Column(VARCHAR(255), nullable=True, default=None)
    organisation = relationship("Organization", back_populates="businesses")
    merchants = relationship("Merchant_", back_populates="business")
    marketplace = relationship("Marketplace")


class Merchant_(Base):
    __tablename__ = "merchants_"
    __table_args__ = (PrimaryKeyConstraint("id", "marketplace_id"),)
    id = Column(Integer, primary_key=True)
    marketplace_id = Column(Integer, ForeignKey("marketplaces.id"), primary_key=True)
    business_id = Column(Integer, ForeignKey("businesses.id"))
    business = relationship("Business", back_populates="merchants")
    shops = relationship("Shop", back_populates="merchant")
    marketplace = relationship("Marketplace")


class Shop(Base):
    __tablename__ = "shops"
    __table_args__ = (PrimaryKeyConstraint("id", "marketplace_id"),)
    id = Column(Integer, primary_key=True)
    marketplace_id = Column(Integer, ForeignKey("marketplaces.id"), primary_key=True)
    merchant_id = Column(Integer, ForeignKey("merchants_.id"))
    merchant = relationship("Merchant_", back_populates="shops")
    storages = relationship("Storage", back_populates="shop")
    marketplace = relationship("Marketplace")


class Storage(Base):
    __tablename__ = "storages"
    __table_args__ = (PrimaryKeyConstraint("id", "marketplace_id"),)
    id = Column(Integer, primary_key=True)
    marketplace_id = Column(Integer, ForeignKey("marketplaces.id"), primary_key=True)
    shop_id = Column(Integer, ForeignKey("shops.id"))
    id_second = Column(BIGINT, nullable=True, default=None)
    type = Column(CHAR(1))
    dbs = Column(CHAR(1))
    express = Column(CHAR(1), nullable=True, default=None)
    alert = Column(VARCHAR(1), nullable=True, default=None)
    binded_warehouse_id = Column(
        CHAR(32), ForeignKey("warehouses.id"), nullable=True, default=None
    )
    second_warehouse_id = Column(
        CHAR(32), ForeignKey("FK_storages_warehouses_2"), nullable=True, default=None
    )
    shop = relationship("Shop", back_populates="storages")
    marketplace = relationship("Marketplace")
    binded_warehouse = relationship("Warehouse")


class Order_(Base):
    __tablename__ = "orders_"
    __table_args__ = (PrimaryKeyConstraint("marketplace_id", "merchant_id", "id"),)
    id = Column(VARCHAR(50), primary_key=True)
    marketplace_id = Column(Integer, ForeignKey("marketplaces.id"), primary_key=True)
    merchant_id = Column(Integer, ForeignKey("merchants_.id"), primary_key=True)
    storage_id = Column(Integer)
    customer_full_name = Column(TEXT, nullable=True, default=None)
    customer_address = Column(TEXT, nullable=True, default=None)
    creation_date = Column(DateTime)
    delivery_date = Column(DateTime, nullable=True, default=None)
    shipment_date = Column(DateTime, nullable=True, default=None)
    add_date = Column(DateTime, nullable=True, default=None)
    finished_date = Column(DateTime, nullable=True, default=None)
    sent_in_telegram = Column(TINYINT(1), nullable=True, default=None)


class Item(Base):
    __tablename__ = "items"
    __table_args__ = (PrimaryKeyConstraint("marketplace_id", "order_id", "good_id"),)
    marketplace_id = Column(Integer, ForeignKey("marketplaces.id"), primary_key=True)
    order_id = Column(VARCHAR(50), ForeignKey("orders_.id"), primary_key=True)
    good_id = Column(VARCHAR(50), ForeignKey("goods.id"), primary_key=True)
    quantity = Column(Integer)
    price = Column(DECIMAL(10, 2))
    final_price = Column(DECIMAL(10, 2))
    status = Column(VARCHAR(255), nullable=True)
    offer = Column(VARCHAR(255), nullable=True)


class Good(Base):
    __tablename__ = "goods"
    marketplace_id = Column(Integer, ForeignKey("marketplaces.id"), primary_key=True)
    id = Column(VARCHAR(50), primary_key=True)
    name = Column(VARCHAR(255))
    slug = Column(VARCHAR(255), nullable=True)


class Offer(Base):
    __tablename__ = "offers"
    id = Column(VARCHAR(50), primary_key=True)
    is_drop = Column(TINYINT(1))


class Product(Base):
    __tablename__ = "products"
    id = Column(CHAR(36), primary_key=True)
    name = Column(VARCHAR(255))
    code = Column(VARCHAR(255), nullable=True, default=None)
    article = Column(VARCHAR(255), nullable=True, default=None)
    last_update = Column(DateTime, nullable=True, default=None)
    stocks = relationship("Stock", back_populates="product")
    barcodes = relationship("Barcode", back_populates="product")


class Stock(Base):
    __tablename__ = "stocks"
    __table_args__ = (PrimaryKeyConstraint("product_id", "warehouse_id"),)
    warehouse_id = Column(CHAR(36), primary_key=True)
    product_id = Column(VARCHAR(255), ForeignKey("products.id"), primary_key=True)
    stock = Column(Integer)
    price = Column(DECIMAL(10, 2))
    last_update = Column(DateTime, nullable=True, default=None)
    is_stone = Column(TINYINT, nullable=True, default=None)
    fixed_price = Column(DECIMAL(10, 2), nullable=True, default=None)
    product = relationship("Product", back_populates="stocks")


class Barcode(Base):
    __tablename__ = "barcodes"
    product_id = Column(VARCHAR(255), ForeignKey("products.id"), primary_key=True)
    type = Column(VARCHAR(255), unique=True)
    code = Column(VARCHAR(255))
    product = relationship("Product", back_populates="barcodes")


class MerchantProduct(Base):
    __tablename__ = "merchants_products"
    __table_args__ = (
        PrimaryKeyConstraint(
            "marketplace_id", "merchant_id", "storage_id", "product_id"
        ),
    )
    marketplace_id = Column(Integer, ForeignKey("marketplaces.id"), primary_key=True)
    merchant_id = Column(Integer, ForeignKey("merchants_.id"), primary_key=True)
    storage_id = Column(BIGINT, ForeignKey("storages.id"), primary_key=True)
    product_id = Column(BIGINT)
    name = Column(VARCHAR(255), nullable=True, default=None)
    shop_sku = Column(VARCHAR(50), nullable=True, default=None)
    offer_id = Column(VARCHAR(255), primary_key=True)
    barcode = Column(VARCHAR(255))
    stock = Column(Integer, nullable=True, default=None)
    price = Column(DECIMAL(10, 2), nullable=True, default=None)
    price_real = Column(DECIMAL(10, 2), nullable=True, default=None)
    price_old = Column(DECIMAL(10, 2), nullable=True, default=None)
    min_price = Column(DECIMAL(10, 2), nullable=True, default=None)
    min_our_price = Column(DECIMAL(10, 2), nullable=True, default=None)
    min_our_price_express = Column(DECIMAL(10, 2), nullable=True, default=None)
    min_price_second = Column(DECIMAL(10, 2), nullable=True, default=None)
    min_price_shop_id = Column(Integer, nullable=True, default=None)
    min_price_express = Column(DECIMAL(10, 2), nullable=True, default=None)
    min_price_express_second = Column(DECIMAL(10, 2), nullable=True, default=None)
    min_price_express_shop_id = Column(Integer, nullable=True, default=None)
    our_minimal = Column(VARCHAR(50))
    only_ours = Column(VARCHAR(50))
    our_shop_count = Column(Integer)
    min_price_last_update = Column(DateTime, nullable=True, default=None)
    visible = Column(CHAR(1), nullable=True, default=None)
    status = Column(VARCHAR(255), nullable=True, default=None)
    last_update = Column(DateTime, nullable=True, default=None)
    merchant = relationship("Merchant_")


class Warehouse(Base):
    __tablename__ = "warehouses"
    id = Column(CHAR(36), primary_key=True)
    name = Column(VARCHAR(255))
    type = Column(VARCHAR(50))
    priority = Column(Integer, nullable=True, default=None)


class AlertOrders(Base):
    __tablename__ = "alert_orders"
    __table_args__ = (PrimaryKeyConstraint("marketplace_id", "merchant_id", "id"),)
    marketplace_id = Column(Integer, ForeignKey("marketplaces.id"), primary_key=True)
    merchant_id = Column(Integer, ForeignKey("merchants_.id"), primary_key=True)
    id = Column(BIGINT, primary_key=True)
    shipment_date_to = Column(DateTime, nullable=True)


class Sticker(Base):
    __tablename__ = "stickers"
    __table_args__ = (PrimaryKeyConstraint("marketplace_id", "order_id", "type"),)
    marketplace_id = Column(Integer, ForeignKey("marketplaces.id"), primary_key=True)
    order_id = Column(VARCHAR(50), ForeignKey("orders_.id"), primary_key=True)
    type = Column(VARCHAR(50), primary_key=True)
    code = Column(VARCHAR(50))
    data = Column(VARCHAR(50))
