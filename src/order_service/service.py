from fastapi import HTTPException
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.cart_service.models import CartItem
from .models import Order
from src.auth_service.ouath import get_current_user, get_session
from src.user_service.models import User
from sqlalchemy import select
import json
from fastapi.websockets import WebSocket, WebSocketDisconnect
from datetime import datetime
from .scheme import OrderResponse, ProductResponse, UpdateStatus, IsPayed
from typing import List


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

    async def send_notification(self, user_id: int, notification: dict):
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                await connection.send_json(notification)

    def disconnect(self, websocket: WebSocket, user_id: int):
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]


# Инициализация менеджера подключений
connection_manager = ConnectionManager()

# WebSocket-соединение для пользователей


class OrderService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_order(self, current_user: User):

        cart_item_query = await self.session.execute(
            select(CartItem)
            .filter(CartItem.is_ready_to_order != True)
            .filter(CartItem.user_id == current_user.id)
        )

        cart_item = cart_item_query.scalars().all()
        if not cart_item:
            raise HTTPException(detail="Not Found", status_code=404)

        for cart in cart_item:
            cart.is_ready_to_order = True

        for product in cart_item:

            new_order = Order(
                product_id=product.product_id,
                user_id=current_user.id,
                is_ready=True,
                status="Ожидание",
            )

            self.session.add(new_order)

        await self.session.commit()

        return {"detail": "Created Sucsesfully"}

    async def get_all_orders(self, current_user: User):

        orders_query = await self.session.execute(
            select(Order)
            .filter(Order.user_id == current_user.id)
            .order_by(Order.created_at.desc())
            .options(selectinload(Order.product))
        )

        orders = orders_query.scalars().all()
        if not orders:
            return []

        response = [
            OrderResponse(
                id=order.id,
                created_at=order.created_at,
                status=order.status,
                is_ready=order.is_ready,
                user_id=order.user_id,
                product=(
                    ProductResponse(
                        id=order.product_id,
                        price=order.product.price,
                        product_photo=order.product.product_photo,
                        product_title=order.product.product_title,
                        description=order.product.description,
                        category=order.product.product_category,
                        created_at=order.product.created_at,
                        is_exist=order.product.is_exist,
                    )
                    if order.product
                    else None
                ),
            )
            for order in orders
        ]

        return response

    async def update_order_status(self, order_id: int, status: UpdateStatus):
        order_query = await self.session.execute(
            select(Order).filter(Order.id == order_id)
        )
        order = order_query.scalars().first()

        if not order:
            raise HTTPException(detail="Order not found", status_code=404)

        order.status = status

        await connection_manager.send_notification(
            order.user_id,
            {
                "order_id": order_id,
                "new_status": order.status,
                "timestamp": datetime.utcnow().isoformat(),
            },
        )

        await self.session.commit()

        return {"Status": "Updated"}


    async def pay_order(self, order_id: int):
        
        product_query = await self.session.execute(

            select(Order)
            .filter(Order.id == order_id)
        )

        product = product_query.scalars().first()
        if not product:
            raise HTTPException(
                detail='Not Found',
                status_code=404
            )
        
        product.status = str(IsPayed.IS_PAYED.value)

        await self.session.commit()

        return {'message':'Payed Succsesfully'}