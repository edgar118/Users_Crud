# -*- coding: utf-8 -*-
from fastapi import FastAPI, Depends
from backend.config import engine, Base, SessionLocal
from sqlalchemy.orm import Session
from backend import routers
from datetime import datetime
from backend.stats import EndpointStats
from backend.routers import get_db
# from backend.crud import record_endpoint_stats

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)
    print("Running default data version scripts")

# Registro del middleware en la aplicación principal
# app.add_middleware(record_endpoint_stats(SessionLocal))

app.include_router(routers.router, prefix="/user", tags=['user'])