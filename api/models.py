from .database import Base
from sqlalchemy import Column, Integer, String


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    prediction = Column(String, nullable=False)