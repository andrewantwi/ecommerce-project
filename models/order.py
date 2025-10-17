

from sqlalchemy import Column, Integer, Numeric, String, DateTime,func
from sqlalchemy.orm import relationship

from core.setup import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String, default="pending_payment")
    created_at = Column(DateTime, default=func.now())

    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    def calculate_total(self):
        """Recalculate total price from order items."""
        self.total_amount = sum(item.total_amount for item in self.items)