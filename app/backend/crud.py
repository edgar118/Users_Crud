from sqlalchemy.orm import Session
from fastapi import HTTPException
from backend.user_model import User
from backend.user_info_model import UserInfo
from backend.schemas import User as UserSchema
from backend.schemas import RequestUser
from datetime import timedelta, datetime
from jose import jwt
from backend import config
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def created_user(db:Session, user=RequestUser):

    hashed_password = pwd_context.hash(user.password)

    add_user = User(
        email = user.email,
        password = hashed_password
    )
    db.add(add_user)

    add_info = UserInfo(
        name = user.name,
        age = user.age,
        user = add_user
    )

    db.add(add_info)
    db.commit()

    return {"message": "ok"}

def update_user(db:Session, user_id, user=UserSchema, ):
    db.query(User).filter(User.id == user_id).update(user.dict(exclude_unset=True))
    db.commit()

    return {"message": "ok"}

def get_user(db:Session):
    users = db.query(User).all()
    return users


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt

def access_token(db, data):
    user = db.query(User).filter(
        User.email == data.email).first()

    if user is None:
        raise HTTPException(
                status_code=422,
                detail="User not Exist",
            )

    if pwd_context.verify(data.password, user.password) is False:
        raise HTTPException(
                status_code=422,
                detail="Error",
            )
    
    user = {"username": data.email}
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}