from fastapi import FastAPI
from datetime import datetime
from zoneinfo import ZoneInfo
from models import Customer, Transaction, Invoice
from db import create_all_tables
from .routers import customers

app = FastAPI(lifespan=create_all_tables)
app.include_router(customers.router)

db_customers: list[Customer] = []
country_timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "PE": "America/Lima"
}

@app.get("/")
async def root():
    return {"Message:": "Hola mundo!"}

@app.get("/time/{iso_code}")
async def getHour(iso_code: str):
    iso = iso_code.upper()
    print(iso)
    timezone_str = country_timezones.get(iso)
    print("time: ", timezone_str)
    tz = ZoneInfo(timezone_str)
    print("tz: ", tz)
    return {"Time": datetime.now(tz) }

@app.post("/transactions")
async def create_transaction(transaction_data: Transaction):
    return transaction_data

@app.post("/invoices")
async def create_invoice(invoice_data: Invoice):
    return invoice_data
