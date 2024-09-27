from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class ProductCategory(Enum):
    STREET_FOOD = 'Street Food'
    NATIONAL_FOOD = 'NATIONAL FOOD'
    KIDS_FOOD = 'Kids Food'
    KOMBO_FOOD = 'Kombo Food'



class ProductResponse(BaseModel):
    
    id: int
    product_title: str
    product_photo: str = None 
    price: int = None
    created_at: datetime
    is_exist: bool
    category: str
    description: str
    number_of_orders: int = 0