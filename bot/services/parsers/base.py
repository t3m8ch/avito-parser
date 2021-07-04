from abc import ABC, abstractmethod
from collections import Iterable

from bot.models import AdModel


class BaseParser(ABC):
    @abstractmethod
    def parse(self, html: str) -> Iterable[AdModel]:
        pass
