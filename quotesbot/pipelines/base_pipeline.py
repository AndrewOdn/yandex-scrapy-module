import json, pika, scrapy
from abc import ABC, abstractmethod
from decimal import Decimal


class Abc_base_pipeline(ABC):
    sku: object
    product_id: object
    out_item: object

    def __init__(self) -> None:
        self.pictures = None
        self.sku_atr = None
        self.sku_name = None
        self.dimensions = None
        self.off_pictures = None
        self.offer_id = None
        self.price = None
        self.shop_name = None
        self.businessId = None
        self.feedId = None
        self.shopId = None
        self.promo = None
        self.vendor = None
        self.name = None
        self.reviewsCount = None
        self.ratingCount = None
        self.description = None
        self.fullDescription = None
        self.rating = None
        self.modelName = None
        self.attributes = None
        self.reasonsToBuy = None
        self.filters = None
        self.category = None
        self.interested = None
        parameters = pika.URLParameters(
            "amqp://admin:2j@@FJhzl0FzahIDDI8!k2akA@localhost:5672/"
        )

        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue="scrapers")

    def process_item(self, item: dict, spider: scrapy.Spider) -> None:
        self.product_id = item["scraping_params"]["product_ids"]
        self.sku = item["scraping_params"]["sku"]
        item["scraping_params"]["marketplace_name"] = "Yandex Market"
        self.out_item = {
            "products_info": [
                {
                    "id": self.product_id,
                    "name": self.name,
                    "reviewsCount": self.reviewsCount,
                    "ratingCount": self.ratingCount,
                    "description": self.description,
                    # "fullDescription": self.fullDescription,
                    "rating": self.rating,
                    # "modelName": self.modelName,
                    "attributes": self.attributes,
                    "pictures": self.pictures,
                    # "reasonsToBuy": self.reasonsToBuy,
                    # "filters": self.filters,
                    "category": self.category,
                    "brand": self.vendor,
                    "skus_info": [
                        {
                            "id": self.sku,
                            "name": self.sku_name,
                            "description": self.description,
                            "dimensions": self.dimensions,
                            "pictures": self.off_pictures,
                            "attributes": self.sku_atr,
                            "interested": self.interested,
                            "offer": [
                                {
                                    "id": self.offer_id,
                                    "price": self.price,
                                    "shop_name": self.shop_name,
                                    "businessId": self.businessId,
                                    "feedId": self.feedId,
                                    "shop_id": self.shopId,
                                    "promo": self.promo,
                                }
                            ],
                        }
                    ],
                }
            ],
            "secondary_info": item["scraping_params"],
        }

    def send_item(self, item: dict) -> None:
        class DecimalEncoder(json.JSONEncoder):
            def default(self, obj):
                # convert it to a string
                if isinstance(obj, Decimal):
                    return str(obj)
                return json.JSONEncoder.default(self, obj)

        json_str = json.dumps(self.out_item, cls=DecimalEncoder)
        self.channel.basic_publish(exchange="", routing_key="scrapers", body=json_str)
