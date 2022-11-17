"""Middlewares for cookies"""
from scrapy import Request


class Ja3ProxiesMiddleware(object):
    """Cookies Middleware"""

    def process_request(self, request: Request, **_):
        """Move proxies to headers for ja3_changer"""
        proxy = request.meta.get("proxy")
        if proxy:
            request.headers["ja3_proxy"] = proxy
            del request.meta["proxy"]
