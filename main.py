from fastapi import FastAPI, HTTPException
from datetime import datetime
from zoneinfo import ZoneInfo
from models import Customer, CustomerCreate, Transaction, Invoice
from db import SessionDep, create_all_tables
from sqlmodel import select

app = FastAPI(lifespan=create_all_tables)

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

@app.get("/customers", response_model=list[Customer])
async def list_customers(session: SessionDep):
    return session.exec(select(Customer)).all()

@app.get("/customer/{user_id}", response_model=Customer)
async def get_customer(user_id: int, session: SessionDep):
    user = session.exec(select(Customer).where(Customer.id == user_id)).first()
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/customers", response_model=Customer)
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@app.post("/transactions")
async def create_transaction(transaction_data: Transaction):
    return transaction_data

@app.post("/invoices")
async def create_invoice(invoice_data: Invoice):
    return invoice_data
