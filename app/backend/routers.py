from fastapi import APIRouter,HTTPException, Path, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from backend.config import SessionLocal
from backend.schemas import User as UserSchema
from backend.schemas import UserList
from backend.schemas import RequestUser

import backend.crud as crud
router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/created')
async def create(
    user: RequestUser,
    db:Session=Depends(get_db)
    ):
    return crud.created_user(db, user)


@router.post("/token")
def login_for_access_token(
    user: UserSchema,
    db: Session = Depends(get_db)
    ):
    return crud.access_token(db, user)


@router.get("/list", response_model=UserList)
async def get_users(db: Session = Depends(get_db)):
    user = crud.get_user(db)
    return {"data": user}

@router.put('/update/{user_id}')
async def update(
    user_id: int,
    user: UserSchema,
    db:Session=Depends(get_db)
    ):
    return crud.update_user(db, user_id, user )



    