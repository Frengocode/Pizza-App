from pydantic import BaseModel
from src.product_service.scheme import ProductResponse
from typing import Optional
from datetime import datetime
from enum import Enum

class OrderResponse(BaseModel):
    id: int
    product: Optional[ProductResponse] = None
    created_at: datetime
    user_id: int
    status: str
    is_ready: bool



class UpdateStatus(Enum):
    IN_PROCESS = 'В Процессе'
    MANY_TIME_FOR_READY = 'Осталось Не сного'
    READY = 'Готов'


class IsPayed(Enum):
    IS_PAYED = 'Оплачен'
    NOT_PAYED = 'Не оплачано'