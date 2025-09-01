from sqlmodel import select
from models import Customer, CustomerUpdate, CustomerCreate
from db import SessionDep
from fastapi import APIRouter, status, HTTPException

router = APIRouter()

@router.get("/customers", response_model=list[Customer], tags=['Customers'])
async def list_customers(session: SessionDep):
    return session.exec(select(Customer)).all()

@router.get("/customers/{customer_id}", response_model=Customer, tags=['Customers'])
async def read_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if customer_db:
        return customer_db
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exist")

@router.delete("/customers/{customer_id}", tags=['Customers'])
async def delete_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exist")
    session.delete(customer_db)
    session.commit()
    return {"Detail": "OK"}

@router.patch("/customers/{customer_id}", response_model=Customer, status_code=status.HTTP_201_CREATED, tags=['Customers'])
async def update_customer(customer_id: int, session: SessionDep, customer_data: CustomerUpdate):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exist")
    data = customer_data.model_dump(exclude_unset=True) # exclude_unset=True solo actualizar los campos que envian
    customer_db.sqlmodel_update(data)
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)
    return customer_db

@router.post("/customers", response_model=Customer, tags=['Customers'])
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer