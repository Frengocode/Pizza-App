from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey
from datetime import datetime
from src.config.database import Base


class CartItem(Base):
    __tablename__ = 'cart_items'

    id: Mapped[int] = mapped_column(Integer, index=True, primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.id', ondelete='CASCADE'))
    product: Mapped["Product"] = relationship("Product", cascade="all, delete")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    is_ready_to_order: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow())
