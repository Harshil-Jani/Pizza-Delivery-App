from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from database import Session, engine
from schemas import SignUpUser, LoginModel
from models import User
from fastapi.exception_handlers import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT


auth_router = APIRouter(prefix="/auth", tags=["auth"])

session = Session(bind=engine)


@auth_router.get("/")
async def root(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )
    return {"message": "Hello World"}


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpUser):
    db_email = session.query(User).filter(User.email == user.email).first()
    if db_email is not None:
        return HTTPException(status_code=400, detail="Email already exists")

    db_username = session.query(User).filter(User.username == user.username).first()
    if db_username is not None:
        return HTTPException(status_code=400, detail="Username already exists")

    new_user = User(
        username=user.username,
        password=generate_password_hash(user.password),
        email=user.email,
        is_staff=user.is_staff,
        is_active=user.is_active,
    )

    session.add(new_user)
    session.commit()
    return new_user


@auth_router.post("/login", status_code=200)
async def login(user: LoginModel, Authorize: AuthJWT = Depends()):
    db_user = session.query(User).filter(User.username == user.username).first()
    print(db_user)
    if db_user and check_password_hash(db_user.password, user.password):
        access_token = Authorize.create_access_token(subject=db_user.username)
        refresh_token = Authorize.create_refresh_token(subject=db_user.username)

        response = {"access_token": access_token, "refresh_token": refresh_token}
        return jsonable_encoder(response)

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Bad username or password"
    )


@auth_router.get("/refresh", status_code=200)
async def refresh_token(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please provide a valid refresh token",
        )

    current_user = Authorize.get_jwt_subject()
    access_token = Authorize.create_access_token(subject=current_user)
    return jsonable_encoder({"access_token": access_token})
