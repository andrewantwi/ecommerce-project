from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from core.setup import Base


class Review(Base):
    __tablename__ = 'review'

    id = Column(Integer, primary_key=True)
    review = Column(String)
    rating = Column(Integer)
    property_id = Column(Integer, ForeignKey('property.id', ondelete='CASCADE'))
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    created_at = Column(String, default=datetime.now().isoformat())

    property = relationship('Property', back_populates='reviews')
    user = relationship('User', back_populates='reviews')
