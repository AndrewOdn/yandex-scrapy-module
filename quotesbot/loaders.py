import gzip
import logging
import shutil
import time
import xml.etree.ElementTree as ET
import pathlib
import random
from pathlib import Path
import requests
import sqlalchemy as sa
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from sqlalchemy import or_

from quotesbot.credentials import DB_CONNECTION_INFO, VLAD_PERSONAL_CONNECTION_INFO
from quotesbot.models.marketplace_bases import MerchantProduct
from quotesbot.models.yandex_bases import Category, Navnode, Product, Sku

process = CrawlerProcess(get_project_settings())


# 'followall' is the name of one of the spiders of the project.


def get_info_for_lists(category_list, category_nid, session):
    work = session.query(Navnode).filter(Navnode.rootNavnode.in_(category_list)).all()
    for job in work:
        if job.id not in category_list:
            category_list.append(job.id)
        if job.category not in category_nid and job.category is not None:
            category_nid.append(job.category)
    return category_list, category_nid


def prepare_to_vlad():
    """запуск функции append_to_vlad"""
    return CreateListFromBd.append_to_vlad([])


def search_new_products():
    """Инициализация класса CreateListFromBd и запуск функции append_item_search"""
    a = CreateListFromBd()
    return a.append_item_search([])


def search_sitemap():
    """запуск функции append_sitemap"""
    return CreateListFromBd.append_sitemap([])


def update_min_prices(sort_type):
    """Инициализация класса CreateListFromBd и запуск функции append_item_update"""
    a = CreateListFromBd()
    return a.append_item_update([], sort_type)


def get_sku_info():
    """Инициализация класса CreateListFromBd и запуск функции append_item_skuinfo"""
    a = CreateListFromBd()
    return a.append_item_skuinfo([])


def get_sku_info_on_stock():
    """Инициализация класса CreateListFromBd и запуск функции append_item_skuinfo"""
    a = CreateListFromBd()
    return a.append_item_skuinfo_on_stock([])


class CreateListFromBd:
    """Класс функций получения параметров для запуска пауков,
    использующий данные из базы yandex-market-prices"""

    def __init__(self):
        self.session = sa.orm.Session(
            bind=sa.create_engine(DB_CONNECTION_INFO),
            autoflush=True,
            autocommit=False,
            expire_on_commit=True,
            info=None,
        )
        # asd
        # engine = sa.create_engine(DB_CONNECTION_INFO)
        # with sa.orm.Session(engine, future=True) as session:
        #    self.session = session

    def append_item_update(self, bd_input, sort_type):
        """Получение данных и генерация списка параметров для паука"""
        sort_type = int(sort_type)
        if sort_type == 2:
            work = (
                self.session.query(Sku)
                .filter(
                    Sku.shop_count != 0 and Sku.shop_count != 1 and Sku.yandex_price_min
                )
                .all()
            )
            for job in work:
                bd_input.append(
                    [
                        str(job.sku) if job.sku else [],
                        str(job.product_id),
                        1,
                        100,
                        job.price_min,
                        job.yandex_price_min,
                    ]
                )
            return bd_input
        elif sort_type == 1:
            work = (
                self.session.query(Sku)
                .filter(or_(Sku.shop_count == 0, Sku.shop_count == None))  # noqa: E711
                .all()
            )
            for job in work:
                bd_input.append(
                    [
                        str(job.sku) if job.sku else [],
                        str(job.product_id),
                        1,
                        100,
                        job.price_min,
                        job.yandex_price_min,
                    ]
                )
            return bd_input
        elif sort_type == 3:
            work = (
                self.session.query(Sku)
                .filter(Category.category_nid == Navnode.id)
                .filter(Navnode.category == "91491")
                .filter(Sku.product_id == Category.product_id)
                # .filter(Sku.shop_count > 1)
                .filter(Sku.brand != "")
                .all()
            )
            for job in work:
                bd_input.append(
                    [
                        str(job.sku) if job.sku else [],
                        str(job.product_id),
                        1,
                        100,
                        job.price_min,
                        job.yandex_price_min,
                    ]
                )
            return bd_input
        elif sort_type == 4:
            work = (
                self.session.query(Sku)
                .filter(Sku.shop_count > 1)
                .filter(Sku.shop_count != 0)
                .filter(Sku.shop_count != None)  # noqa: E711
                .all()
            )
            for job in work:
                bd_input.append(
                    [
                        str(job.sku) if job.sku else [],
                        str(job.product_id),
                        1,
                        100,
                        job.price_min,
                        job.yandex_price_min,
                    ]
                )
            return bd_input
        elif 20 <= sort_type < 30:
            i = sort_type - 20
            work = (
                self.session.query(
                    Sku.sku, Sku.product_id, Sku.price_min, Sku.yandex_price_min
                )
                .filter(Sku.shop_count > 1)
                .filter(Sku.shop_count != 0)
                .filter(Sku.shop_count != None)  # noqa: E711
                .limit(400000)
                .offset(i * 400000)
            )
            for job in work:
                bd_input.append(
                    [
                        str(job.sku) if job.sku else [],
                        str(job.product_id),
                        1,
                        100,
                        job.price_min,
                        job.yandex_price_min,
                    ]
                )
            return bd_input
        elif 30 <= sort_type < 40:
            i = sort_type - 30
            work = (
                self.session.query(
                    Sku.sku, Sku.product_id, Sku.price_min, Sku.yandex_price_min
                )
                .filter(Sku.shop_count == 1)
                .limit(3000000)
                .offset(i * 3000000)
            )
            for job in work:
                bd_input.append(
                    [
                        str(job.sku) if job.sku else [],
                        str(job.product_id),
                        1,
                        100,
                        job.price_min,
                        job.yandex_price_min,
                    ]
                )
            return bd_input

    def append_item_search(self, bd_input):
        """Получение данных и генерация списка параметров для паука"""
        try:
            navnode = (
                self.session.query(Navnode)
                .filter(Navnode.isLeaf == 1)
                .order_by(Navnode.offersCount)
                .all()
            )
        except Exception as e:
            logging.error("Lost conn to dabase")
            logging.error(e)
            time.sleep(1)
            pass
        for nav in navnode:
            bd_input.append([nav.id, nav.category, 1, 35])
        return bd_input

    def append_item_skuinfo(self, bd_input):
        """Получение данных и генерация списка параметров для паука"""
        work = (
            self.session.query(Product)
            .join(Sku, Sku.product_id == Product.id, isouter=True)
            .filter(Product.title == None)  # noqa: E711
            .all()
        )
        print(len(work))
        for job in work:
            # product = job.Product
            bd_input.append(
                [
                    str(job.id),
                    str(""),
                    str(""),
                    "https://market.yandex.ru/product/" + str(job.id),
                ]
            )
        return bd_input

    def append_item_skuinfo_on_stock(self, bd_input):
        """Получение данных и генерация списка параметров для паука"""
        work = self.session.query(
            Sku.sku, Sku.product_id, Sku.price_min, Sku.yandex_price_min
        ).all()  # noqa: E711
        for job in work:
            # product = job.Product
            bd_input.append(
                [
                    str(job.product_id),
                    str(job.sku),
                    str(""),
                    "https://market.yandex.ru/product/"
                    + str(job.product_id)
                    + "&sku="
                    + str(job.sku),
                ]
            )
        return bd_input

    @staticmethod
    def append_sitemap(bd_input):
        """Получение данных и генерация списка параметров для паука"""
        dir_path = pathlib.Path.cwd()
        path = Path(dir_path, "proxies", "proxies_webshare.txt")

        proxy_list = []
        with open(path) as f:
            for line in f:
                line = line.replace("\n", "")
                proxy_list.append("http://" + line)

        def get_url_from_url(url, proxy_list):
            """Получение ссылок на товары из архива"""

            def proxy_request(url, ip_addresses):
                try:
                    proxy = random.randint(0, len(ip_addresses) - 1)
                    proxies = {"http": ip_addresses[proxy]}
                    response = requests.get(url, proxies=proxies, stream=True)
                    if response.status_code < 300:
                        logging.info(
                            f"Proxy currently being used: {ip_addresses[proxy]}"
                        )
                        logging.info(f"url is {url}")
                        return response
                    else:
                        logging.warning(f"{response.text}")
                        time.sleep(10)
                        logging.warning("БЕДЫ С ЗАПРОСОМ")
                        logging.warning(f"response not 200: {ip_addresses[proxy]}")
                except Exception:
                    logging.info(f"Proxy down: {ip_addresses[proxy]}")

            response = proxy_request(url, proxy_list)
            if response.status_code == 200:
                with open("target_path2", "wb") as f:
                    f.write(response.raw.read())
            with gzip.open("target_path2", "rb") as f_in:
                with open("x_file_name2.xml", "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)

            tree = ET.parse("x_file_name2.xml")
            root = tree.getroot()
            # printing the text contained within
            # first subtag of the 5th tag from
            # the parent
            for i in range(len(root)):
                yield root[i][0].text

        def get_url_from_request(proxy_list):
            """Получение архивов с ссылками на товары"""
            response = requests.get(
                "https://m.market.yandex.ru/sitemap/sitemap-model_main.xml", stream=True
            )

            text = response.text
            ccurl = 0
            while str.find(text, "<loc>https://m.market.yandex.ru/sitemap/") != -1:
                ccurl = ccurl + 1
                url = text[
                    str.find(text, "<loc>https://m.market.yandex.ru/sitemap/")
                    + 5 : str.find(text, "</loc>")
                ]
                text = text[str.find(text, "</loc>") + 6 :]
                if ccurl >= 579:
                    g = get_url_from_url(url, proxy_list)
                    bd_input.append(g)

        get_url_from_request(proxy_list)
        return bd_input

    @staticmethod
    def append_to_vlad(bd_input):
        """Получение данных и генерация списка параметров для паука"""
        session = sa.orm.Session(
            bind=sa.create_engine(VLAD_PERSONAL_CONNECTION_INFO),
            autoflush=True,
            autocommit=False,
            expire_on_commit=True,
            info=None,
        )
        work = (
            session.query(MerchantProduct)
            .filter(MerchantProduct.marketplace_id == 2)
            .group_by(MerchantProduct.product_id)
            .all()
        )
        for job in work:
            # product = job.Product
            bd_input.append(
                [
                    str(job.marketplace_id),
                    str(job.merchant_id),
                    str(job.storage_id),
                    str(job.product_id),
                    1,
                    100,
                ]
            )
        return bd_input
