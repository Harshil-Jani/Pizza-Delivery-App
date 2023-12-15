from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy_utils.types import ChoiceType
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(50), unique=True)
    password = Column(Text, nullable=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    orders = relationship("Order", back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>"


class Order(Base):
    ORDER_STATUS = (
        ("PENDING", "pending"),
        ("ACCEPTED", "accepted"),
        ("REJECTED", "rejected"),
        ("DELIVERED", "delivered"),
    )
    PIZZA_SIZE = (
        ("SMALL", "small"),
        ("MEDIUM", "medium"),
        ("LARGE", "large"),
        ("EXTRA_LARGE", "extra_large"),
    )

    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    order_status = Column(ChoiceType(ORDER_STATUS), default="PENDING")
    pizza_size = Column(ChoiceType(PIZZA_SIZE), default="SMALL")
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="orders")

    def __repr__(self):
        return f"<Order {self.name}>"
