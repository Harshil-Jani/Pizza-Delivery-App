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


@order_router.get("/all_orders", status_code=status.HTTP_200_OK)
async def list_all_orders(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()

    if user.is_staff == True:
        orders = session.query(Order).all()
        return jsonable_encoder(orders)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You are not authorized to view this page",
    )


@order_router.get("/order/{id}")
async def get_order_by_id(id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()

    if user.is_staff == True:
        order = session.query(Order).filter(Order.id == id).first()
        return jsonable_encoder(order)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You are not authorized to view this page",
    )


@order_router.get("/user_orders")
async def get_user_orders(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()
    return jsonable_encoder(user.orders)


@order_router.get("/user_order/{id}")
async def get_user_order_by_id(id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()
    orders = user.orders
    for order in orders:
        if order.id == id:
            return jsonable_encoder(order)
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="This order is not found",
    )
