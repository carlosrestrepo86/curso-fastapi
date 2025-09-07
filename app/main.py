from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Request, status
from datetime import datetime
import time
import os
from zoneinfo import ZoneInfo
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from models import Customer
from db import create_all_tables
from .routers import customers, invoices, transactions, plans
from dotenv import load_dotenv

app = FastAPI(lifespan=create_all_tables)
app.include_router(customers.router)
app.include_router(invoices.router)
app.include_router(transactions.router)
app.include_router(plans.router)

security = HTTPBasic()
load_dotenv()

user = os.getenv("USER")
password = os.getenv("PASSWORD")

# Imprimir todos los headers que están enviando a todos lo endpoints
@app.middleware("http")
async def log_header(request: Request, call_next):
    print("========== HEADERS ===========")
    
    for key, value in request.headers.items():
        print(f"{key}: {value}")
    print("==============================")
    
    response = await call_next(request)
    return response



@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Request: {request.url} completed in: {process_time:.4f} seconds")
    return response

db_customers: list[Customer] = []
country_timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "PE": "America/Lima"
}

@app.get("/")
async def root(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    if credentials.username == user and credentials.password == password:
        return {"Message:": f"Hola , {credentials.username}"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user")

@app.get("/time/{iso_code}")
async def getHour(iso_code: str):
    iso = iso_code.upper()
    print(iso)
    timezone_str = country_timezones.get(iso)
    print("time: ", timezone_str)
    tz = ZoneInfo(timezone_str)
    print("tz: ", tz)
    return {"Time": datetime.now(tz) }

