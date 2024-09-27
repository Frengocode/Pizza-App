from src.config.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime
from datetime import datetime
from src.order_service.models import Order

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, index=True, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow())
    orders: Mapped["Order"] = relationship('Order', back_populates='user')