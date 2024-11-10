import bcrypt
from fastapi import APIRouter, HTTPException, Depends, Response
from sqlalchemy.orm import Session

from models.user import User
from database.database import get_db
from utils.security import genToken, checkToken
from schemas.user import UserRegisterForm, UserLoginForm, UserResponse


router = APIRouter(prefix="/api/v1/auth", tags=["Users"])


@router.post("/signup", response_model=UserResponse)
async def signup(
    response: Response, user_req: UserRegisterForm, db: Session = Depends(get_db)
) -> UserResponse:
    if db.query(User).filter(User.email == user_req.email).first():
        raise HTTPException(status_code=400, detail="User already exist")
    # hashind password
    salt = bcrypt.gensalt(10)
    hash_password = bcrypt.hashpw(user_req.password.encode(), salt).decode()

    new_user = User(
        username=user_req.username,
        email=user_req.email,
        hashed_password=hash_password,
    )
    db.add(new_user)
    db.commit()
    genToken(new_user.id, response=response)
    return new_user


@router.post("/login", response_model=UserResponse)
async def login(
    response: Response, user_req: UserLoginForm, db: Session = Depends(get_db)
) -> UserResponse:
    user = db.query(User).filter(User.email == user_req.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    is_password = bcrypt.checkpw(
        user_req.password.encode(), user.hashed_password.encode()
    )

    if not is_password:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    genToken(user.id, response=response)
    return user


@router.get("/logout")
async def logout(response: Response):
    response.delete_cookie("authorisation")
    return {"data": "Logged out successfully"}


@router.get("/users", response_model=list[UserResponse])
async def get_users(
    is_authorised: bool = Depends(checkToken), db: Session = Depends(get_db)
) -> list[UserResponse]:
    users = db.query(User).all()
    return users
