from pydantic import BaseModel
from src.product_service.scheme import ProductResponse
from typing import Optional
from datetime import datetime

class CartItemResponse(BaseModel):

    id: int
    product: Optional[ProductResponse] = None
    created_at: datetime
    is_ready_to_order: bool
    user_id: int
    all_price: Optional[int] = 0