from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from models import User, Order
from schemas import OrderModel
from database import Session, engine
from fastapi.encoders import jsonable_encoder

order_router = APIRouter(prefix="/orders", tags=["orders"])
session = Session(bind=engine)


@order_router.get("/")
async def root(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"message": "Hello World"}


@order_router.post("/create", status_code=status.HTTP_201_CREATED)
async def place_an_order(order: OrderModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()
    order = Order(
        quantity=order.quantity,
        order_status=order.order_status,
        pizza_size=order.pizza_size,
        user_id=user.id,
    )
    session.add(order)
    session.commit()
    response = {
        "pizza_size": order.pizza_size,
        "quantity": order.quantity,
        "order_status": order.order_status,
        "id": order.id,
    }

    return jsonable_encoder(response)
