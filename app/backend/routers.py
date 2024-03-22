from fastapi import APIRouter,HTTPException, Path, Depends, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from backend.config import SessionLocal
from backend.schemas import User as UserSchema
from backend.schemas import login
from backend.schemas import UserList
from backend.schemas import RequestUser
import backend.crud as crud
from httpx import AsyncClient
from fastapi.responses import JSONResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/created')
def create(
    user: RequestUser,
    db:Session=Depends(get_db),
    request: Request = None
    ):
    return crud.created_user(db, user, request)


@router.post("/token")
def login_for_access_token(
    user: login,
    db: Session = Depends(get_db)
    ):
    return crud.access_token(db, user)

@router.get("/list")
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

@router.get("/get_client_ip")
async def get_client_public_ip(
    db:Session=Depends(get_db),
    request: Request = None
):
    public_ip = crud.stast_endpoint(db, request)
    return public_ip