from fastapi import APIRouter, Depends
from .service import OrderService, WebSocket, connection_manager
from src.auth_service.ouath import get_current_user, get_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.user_service.models import User
from .scheme import OrderResponse, UpdateStatus


order_service = APIRouter(tags=["Order"])


@order_service.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await connection_manager.connect(websocket, user_id)
    try:
        while True:
            await websocket.receive_text()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connection_manager.disconnect(websocket, user_id)


@order_service.post("/create-order/")
async def create_order(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = OrderService(session=session)
    return await service.create_order(current_user=current_user)


@order_service.get("/get-all-user-orders/", response_model=list[OrderResponse])
async def get_all_orders(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = OrderService(session=session)
    return await service.get_all_orders(current_user=current_user)


@order_service.patch("/update-status/{order_id}", response_model=dict)
async def update_status(
    status: UpdateStatus,
    order_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = OrderService(session=session)

    status_query = status.value

    return await service.update_order_status(order_id=order_id, status=status_query)


@order_service.patch('/pay-order/{order_id}/')
async def pay_order(order_id: int, session: AsyncSession = Depends(get_session)):
    service = OrderService(session=session)
    return await service.pay_order(order_id=order_id)