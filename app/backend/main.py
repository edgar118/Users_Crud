# -*- coding: utf-8 -*-
from fastapi import FastAPI
from backend.config import engine, Base
from sqlalchemy.orm import Session
from backend import routers

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)
    print("Running default data version scripts")

app.include_router(routers.router, prefix="/user", tags=['user'])