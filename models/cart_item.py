from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from core.setup import Base


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)


    cart = relationship("Cart", back_populates="cart_items")
    product = relationship("Product")

    def to_dict(self):
        return {
            "id": self.id,
            "cart_id": self.cart_id,
            "user_id":self.cart.user_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "price": self.price,
            "total_price": self.total_price,
        }

    def update_total_price(self):
        """Calculate total price based on quantity."""
        self.total_price = self.quantity * self.price