import re
from decimal import Decimal
from typing import Iterable, Optional

from bs4 import BeautifulSoup
from urlpath import URL

from bot.misc.models import AdModel, SubscriptionModel
from bot.services.parsers.base import BaseParser


class AvitoParser(BaseParser):
    def validate_url(self, url: str) -> bool:
        url = URL(url)
        return bool(
            re.search(r"([a-z0-9\.]|^)avito\.ru$", str(url.hostname))
        )

    def correct_url(self, url: str) -> str:
        is_mobile_version = "m.avito.ru" in url
        if is_mobile_version:
            return url.replace("m.", "", 1)  # Switch mobile version to desktop

        return url

    def parse(self, html: str, subscription: Optional[SubscriptionModel] = None) \
            -> Iterable[AdModel]:
        soup = BeautifulSoup(html, "lxml")
        items = soup.find_all(class_="iva-item-root-G3n7v")
        for i in items:
            title = i.find("h3").text.strip()

            price = i.find(class_="price-text-1HrJ_").text.replace(" ", "")[:-1]
            price = Decimal(price) if price.isnumeric() else None

            url = i.find(class_="link-link-39EVK").get("href")
            url = f"https://avito.ru{url}"

            yield AdModel(
                title=title,
                price=price,
                url=url,
                subscription=subscription
            )
