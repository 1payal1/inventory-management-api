from sqlalchemy import Column, Integer, String, Float
from app.database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    quantity = Column(Integer, default=0)
    price = Column(Float, nullable=False)