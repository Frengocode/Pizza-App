from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey
from datetime import datetime
from src.config.database import Base


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(Integer, index=True, primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.id', ondelete=('CASCADE')))
    product: Mapped["Product"] = relationship('Product', back_populates = 'orders')
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    user: Mapped["User"] = relationship("User", back_populates='orders')
    is_ready: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow())
    status: Mapped[str] = mapped_column(String, nullable=True)