from fastapi import APIRouter, status
from database import Session, engine
from schemas import SignUpUser
from models import User
from fastapi.exception_handlers import HTTPException
from bcrypt import hashpw, gensalt

auth_router = APIRouter(prefix="/auth", tags=["auth"])

session = Session(bind=engine)


@auth_router.get("/")
async def root():
    return {"message": "Hello World"}


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpUser):
    db_email = session.query(User).filter(User.email == user.email).first()
    if db_email is not None:
        return HTTPException(status_code=400, detail="Email already exists")

    db_username = session.query(User).filter(User.username == user.username).first()
    if db_username is not None:
        return HTTPException(status_code=400, detail="Username already exists")

    salt = gensalt()
    hashed_pw = hashpw(user.password.encode(), salt)

    new_user = User(
        username=user.username,
        password=hashed_pw,
        email=user.email,
        is_staff=user.is_staff,
        is_active=user.is_active,
    )

    session.add(new_user)
    session.commit()
    return new_user
