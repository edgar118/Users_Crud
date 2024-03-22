import requests
from sqlalchemy.orm import Session
from fastapi import HTTPException
from backend.user_model import User
from backend.user_info_model import UserInfo
from backend.stats import EndpointStats
from backend.schemas import User as UserSchema
from backend.schemas import RequestUser
from datetime import timedelta, datetime
from jose import jwt
from backend import config
from passlib.context import CryptContext
from fastapi import Request


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_public_ipv2():
    try:
        ip_response = requests.get("https://api64.ipify.org?format=json")
        ip_response.raise_for_status()
        ip_data = ip_response.json()
        ip = ip_data["ip"]
        print('167.0.231.131')
        
        location_response = requests.get(f"https://ipinfo.io/{ip}/json")
        location_response.raise_for_status()
        data_location = location_response.json()
        
        return data_location
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def stast_endpoint(db:Session, request: Request):
    start_time = datetime.now()
    end_time = datetime.now()
    elapsed_time = (end_time - start_time).total_seconds() * 1000

    endpoint_path = request.url.path
    user = get_public_ipv2()

    stats = db.query(EndpointStats).filter_by(endpoint=endpoint_path).first()
    if stats:
        stats.count += 1
        stats.total_time = elapsed_time
        stats.location=user['city'],
        stats.region=user['region'],
        stats.country=user['country']
    else:
        stats = EndpointStats(
            endpoint=endpoint_path,
            count=1,
            total_time=elapsed_time,
            location=user['city'],
            region=user['region'],
            country=user['country']
            )
        db.add(stats)

def created_user(db:Session, user: RequestUser, request: Request):

    stast_endpoint(db, request)

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