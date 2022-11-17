import logging
import uuid

import scrapy
from scrapy.http.request.json_request import JsonRequest

from quotesbot import loaders


class ToUpdateSpider(scrapy.Spider):
    """Паук для обновления основных параметров товара
    с Yandex Market`a(Цена, интересы, отзывы и тд)
    При вызове паука обязательно должен передаваться аргумент loaders_type
    1 - Проход по всем записям в таблице
    2 - Проход по shop_count != 0 and shop_count != 1
    3 - Проход по shop_count != 0 and shop_count != 1 and yandex_price_min
    scrapy crawl toupdate -a loaders_type=a
    """

    custom_settings = {
        "ITEM_PIPELINES": {"quotesbot.pipelines.toupdate.UpdatePipeline": 300}
    }

    name = "toupdate"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        logging.info(f"Spider start with loaders_type={self.loaders_type}")
        logging.info("Preparing loaders")
        self.parse_params = loaders.update_min_prices(self.loaders_type)
        self.headers = {
            "Content-Type": "application/json",
            "api-platform": "ANDROID",
            "X-Test-Id": "0,0,",
            "X-App-Version": "3.98",
            "User-Agent": "Beru/3.98 (Android/7.1.2; A5010/OnePlus)",
            "X-Market-Rearrfactors": (
                ";market_cashback_for_not_ya_plus=1;"
                "market_promo_blue_cheapest_as_gift_4=1;"
                "market_promo_blue_flash=1;market_promo_"
                "blue_generic_bundle=1;market_rebranded=1;"
                "market_white_cpa_on_blue=2;show_credits_on_white=1;"
                "sku_offers_show_all_alternative_offers=1"
            ),
            "X-Region-Id": "213",
            "Host": "ipa.market.yandex.ru",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
        self.version = 1
        self.name = "resolveSkuInfo%2CresolveProductInfo%2CresolveProductOffers"
        logging.info(f"Start start_requests, total - {len(self.parse_params)} requests")

    def start_requests(self):
        """Отправление request на Yandex Market"""  # noqa: E501
        for i in range(0, len(self.parse_params)):
            self.device_id = str(uuid.uuid4())
            self.url = (
                f"https://ipa.market.yandex.ru/api/v{self.version}"
                f"/?name={self.name}&uuid={self.device_id}"
            )
            count = int(self.parse_params[i][3])
            page = int(self.parse_params[i][2])
            sku_ids = [str(self.parse_params[i][0])]
            product_ids = [str(self.parse_params[i][1])]
            price_min = self.parse_params[i][4]
            yandex_price_min = self.parse_params[i][5]
            main_data = {
                "loaders_type": self.loaders_type,
                "method": self.name,
                "sku": sku_ids[0],
                "product_ids": product_ids[0],
                "page": page,
                "count": count,
                "price_min": price_min,
                "yandex_price_min": yandex_price_min,
            }
            j = {
                "params": [
                    {
                        "productIds": product_ids,
                        "skuIds": sku_ids,
                        "showCredits": [True],
                        "showInstallments": [False],
                        "billingZone": "productRecommendedOffers",
                        "specificationSet": ["msku-friendly"],
                        "cpa": "real",
                        "new-picture-format": "1",
                        "get-category-path": False,
                        "showPreorder": True,
                    },
                    {
                        "productIds": [product_ids[0]],
                        "billingZone": "productRecommendedOffers",
                        "specificationSet": ["full"],
                        "cpa": "real",
                        "new-picture-format": "1",
                        "showPreorder": True,
                    },
                    {
                        "skuIds": sku_ids,
                        "productIds": product_ids,
                        "promoByCartEnabled": True,
                        "showDigitalDsbsGoods": True,
                        "cartSnapshot": [],
                        "billingZone": "productOffersWithSort",
                        "page": 1,
                        "showCredits": True,
                        "showInstallments": True,
                        "enableJumpTable": False,
                        "how": "aprice",
                        "showUrls": ["cpa"],
                        "adult": 1,
                        "onstock": 1,
                        "count": 3,
                        "cpa": "real",
                        "showPreorder": True,
                        "use-virt-shop": 0,
                        "showTableSize": True,
                        "glfilter": [],
                        "fb-based-size-table": 1,
                    },
                ]
            }
            yield JsonRequest(
                url=self.url,
                callback=self.parse,
                data=j,
                headers=self.headers,
                meta=main_data,
            )

    def parse(self, response):
        """Получение и форматирование response от Yandex Market`a"""  # noqa: E501
        try:
            response_dict = response.json()
            response_dict["scraping_params"] = response.meta
            yield response_dict
        except Exception:
            """yandex недоверяет прокси"""
            logging.warning("Spider response.json fail")
