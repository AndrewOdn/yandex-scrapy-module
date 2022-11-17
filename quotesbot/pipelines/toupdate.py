import logging
import time
from datetime import datetime
from decimal import *
from typing import Optional, Any

import pika
import scrapy
import sqlalchemy as sa
import telebot
from ..pipelines.base_pipeline import Abc_base_pipeline
from quotesbot import credentials
from quotesbot.models.yandex_bases import Category, Navnode, Product, Sku, Yandex


class SortMethods:
    """Класс функций обработки json'a c предложениями"""

    @staticmethod
    def get_promo_price(offer):
        if "promos" in offer and offer["promos"]:
            for promo in offer["promos"]:
                if "type" in promo:
                    if promo["type"] in ["promo-code", "direct-discount"]:
                        price_new = int(
                            promo["itemsInfo"]["price"]["value"]
                            if promo["type"] == "direct-discount"
                            else promo["itemsInfo"]["price"]["currentPrice"]["value"]
                        )
                        if offer["price"]["value"] <= price_new:
                            continue
                        if (
                            "value_old" not in offer["price"]
                            or price_new < offer["price"]["value"]
                        ):
                            offer["price"]["value_old"] = offer["price"]["value"]
                            offer["price"]["value"] = price_new
                            offer["price"]["promo"] = (
                                promo["promoCode"] if "promoCode" in promo else None
                            )
                    else:
                        pass
                        # print('Promo type', promo['type'], sku.product_id, sku.sku)
        return offer

    @staticmethod
    def get_sorted_offers(id: int, sku: str, offers: list) -> list:

        return sorted(
            list(
                filter(
                    lambda offer: ("marketSku" in offer and offer["marketSku"] == sku)
                    or (offer["productId"] == id),
                    offers,
                )
            ),
            key=lambda d: d["price"]["value_old"]  # type: ignore
            if "value_old" in d["price"]
            else d["price"]["value"],
        )


class UpdatePipeline(Abc_base_pipeline):
    """Класс pipeline для паука toupdate.py"""

    ratingCount: Optional[Any]
    reviewsCount: Optional[Any]

    chat_id = int(credentials.CHAT_ID)
    bot_token = str(credentials.BOT_TOKEN)

    def __init__(self) -> None:
        super(UpdatePipeline, self).__init__()

    def process_item(self, item: dict, spider: scrapy.Spider) -> None:
        """ """
        super(UpdatePipeline, self).process_item(item, spider)

        if "product" in item["collections"]:
            if item["collections"]["product"]:
                self.reviewsCount = (
                    item["collections"]["product"][0]["reviewsCount"]
                    if "reviewsCount" in item["collections"]["product"][0]
                    else None
                )
                self.ratingCount = (
                    item["collections"]["product"][0]["ratingCount"]
                    if "ratingCount" in item["collections"]["product"][0]
                    else None
                )
                self.attributes = (
                    item["collections"]["product"][0]["specs"]["full"]
                    if "full" in item["collections"]["product"][0]["specs"]
                    else None
                )
                self.description = (
                    item["collections"]["product"][0]["description"]
                    if "description" in item["collections"]["product"][0]
                    else None
                )
                # self.fullDescription = item["collections"]['product'][0]['fullDescription'] if "fullDescription" in \
                #                                                                           item["collections"][
                #                                                                               'product'][
                #                                                                               0] else None
                # self.modelName = item["collections"]['product'][0]['modelName']['raw'] if "modelName" in \
                #                                                                      item["collections"]['product'][
                #                                                                          0] else None
                self.pictures = (
                    item["collections"]["product"][0]["pictures"]
                    if "pictures" in item["collections"]["product"][0]
                    else None
                )
                self.rating = (
                    item["collections"]["product"][0]["rating"]
                    if "rating" in item["collections"]["product"][0]
                    else None
                )
                # self.reasonsToBuy = item["collections"]['product'][0]['reasonsToBuy'] if "reasonsToBuy" in \
                #                                                                     item["collections"]['product'][
                #                                                                         0] else None
                self.name = (
                    item["collections"]["product"][0]["titles"]["raw"]
                    if "titles" in item["collections"]["product"][0]
                    else None
                )
                # self.filters = item["collections"]['product'][0]['filters'] if "filters" in item["collections"]['product'][
                #     0] else None
        if "category" in item["collections"]:
            if item["collections"]["category"]:
                self.category = item["collections"]["category"]
                for cat in self.category:
                    if "entity" in cat:
                        del cat["entity"]
                    if "kinds" in cat:
                        del cat["kinds"]
                    if "cpaType" in cat:
                        del cat["cpaType"]
                    if "nid" in cat:
                        del cat["nid"]
                    if "slug" in cat:
                        del cat["slug"]
                    if "type" in cat:
                        del cat["type"]
                        del cat["isLeaf"]

        if "vendor" in item["collections"]:
            if item["collections"]["vendor"]:
                self.vendor = item["collections"]["vendor"][0]
                if "filter" in self.vendor:
                    del self.vendor["filter"]
                if "entity" in self.vendor:
                    del self.vendor["entity"]
                if "logo" in self.vendor:
                    del self.vendor["logo"]
                if "slug" in self.vendor:
                    del self.vendor["slug"]
                if "website" in self.vendor:
                    del self.vendor["website"]
        try:
            if "reasonsToBuy" in item["collections"]["product"][0]:
                self.interested = str(item["collections"]["product"][0]["reasonsToBuy"])
                if str.find(self.interested, "'type': 'statFactor'") != -1:
                    self.interested = self.interested[
                        : str.rfind(self.interested, "'type': 'statFactor'")
                    ]
                    self.interested = self.interested[: str.rfind(self.interested, ",")]
                    self.interested = self.interested[
                        str.rfind(self.interested, ":") + 2 :
                    ]
                    self.interested = int(self.interested)  # type: ignore
        except Exception:
            self.interested = None  # type: ignore
        if "sku" in item["collections"]:
            if "specs" in item["collections"]["sku"]:
                self.sku_atr = (
                    item["collections"]["sku"]["specs"]
                    if "specs" in item["collections"]["sku"]
                    else None
                )
        if "offer" in item["collections"]:
            offers = SortMethods.get_sorted_offers(
                self.product_id, self.sku, item["collections"]["offer"]
            )
            if offers:
                self.sku_name = (
                    offers[0]["modelAwareTitles"]["raw"]
                    if "modelAwareTitles" in offers[0]
                    else None
                )
                self.dimensions = (
                    offers[0]["dimensions"] if "dimensions" in offers[0] else None
                )
                if self.dimensions:
                    self.dimensions["weight"] = (
                        offers[0]["weight"] if "weight" in offers[0] else None
                    )
                self.description = (
                    offers[0]["description"] if "description" in offers[0] else None
                )
                self.off_pictures = (
                    offers[0]["pictures"] if "pictures" in offers[0] else None
                )
                if self.off_pictures:
                    for pic in self.off_pictures:
                        del pic["entity"]
                        del pic["signatures"]
                        del pic["original"]["namespace"]
                        del pic["original"]["groupId"]
                self.out_item["products_info"][0]["skus_info"][0]["offer"].pop(0)
                for offer in offers:
                    shopId = offer["shopId"] if "shopId" in offer else None
                    price = offer["price"] if "price" in offer else None
                    promo = offer["promos"] if "promos" in offer else None
                    offer_id = offer["id"] if "id" in offer else None
                    for sh in item["collections"]["shop"]:
                        if sh["id"] == shopId:
                            shop_name = sh["shopName"] if "shopName" in sh else None
                            businessId = (
                                sh["businessId"] if "businessId" in sh else None
                            )
                            feedId = sh["feedId"] if "feedId" in sh else None
                    temp_off = {
                        "id": offer_id,
                        "price": price,
                        "shop_name": shop_name,
                        "businessId": businessId,
                        "feedId": feedId,
                        "shop_id": shopId,
                        "promo": promo,
                    }
                    self.out_item["products_info"][0]["skus_info"][0]["offer"].append(
                        temp_off
                    )
        super(UpdatePipeline, self).send_item(item)