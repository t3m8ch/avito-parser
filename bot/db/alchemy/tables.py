from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class AdTable(Base):
    __tablename__ = "ad"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    price = Column(Numeric, nullable=True)
    url = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return f"AdTable(" \
               f"id={self.id!r}, " \
               f"name={self.title!r}, " \
               f"price={self.price!r}, " \
               f"url={self.url!r})"


class SubscriptionTable(Base):
    __tablename__ = "subscription"

    chat_id = Column(Integer, primary_key=True, autoincrement=False, nullable=False)
    url = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return f"SubscriptionTable(" \
               f"chat_id={self.chat_id!r}, " \
               f"url=({self.url!r})"
