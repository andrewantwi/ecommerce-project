from datetime import datetime

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from core.setup import Base


class Property(Base):
    __tablename__ = 'property'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    price = Column(Integer)
    location = Column(String)
    created_at = Column(String, default=datetime.now().isoformat())

    reviews = relationship('Review', back_populates='property')

    def __str__(self) -> str:
        self.name
