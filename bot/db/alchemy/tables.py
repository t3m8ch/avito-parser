from sqlalchemy import Column, Integer, String, Numeric, UniqueConstraint, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class AdTable(Base):
    __tablename__ = "ad"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    price = Column(Numeric, nullable=True)
    url = Column(String, nullable=False)
    subscription_id = Column(
        Integer,
        ForeignKey("subscription.id", ondelete="CASCADE"),
        nullable=False
    )

    __table_args__ = (UniqueConstraint("subscription_id", "url"),)

    def __repr__(self):
        return f"AdTable(" \
               f"id={self.id!r}, " \
               f"title={self.title!r}, " \
               f"price={self.price!r}" \
               f"url={self.url!r}, " \
               f"subscription_id={self.subscription!r})"


class SubscriptionTable(Base):
    __tablename__ = "subscription"

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, nullable=False)
    url = Column(String, nullable=False)

    ads = relationship("AdTable", cascade="all, delete")

    __table_args__ = (UniqueConstraint("chat_id", "url"),)

    def __repr__(self):
        return f"SubscriptionTable(" \
               f"id={self.id!r}, " \
               f"chat_id={self.chat_id!r}, " \
               f"url=({self.url!r})"
