from sqlmodel import select
from models import Customer, CustomerPlan, CustomerUpdate, CustomerCreate, Plan, StatusEnum
from db import SessionDep
from fastapi import APIRouter, Query, status, HTTPException

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

@router.post("/customers", response_model=Customer, status_code=status.HTTP_201_CREATED ,tags=['Customers'])
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@router.post("/customers/{customer_id}/plans/{plan_id}", tags=['Customers'])
async def subscribe_customer_to_plan(customer_id: int, plan_id: int, session: SessionDep, plan_status: StatusEnum = Query()): #Query parametro en la URL
    customer_db = session.get(Customer, customer_id)
    plan_db = session.get(Plan, plan_id)
    
    if not customer_db or not plan_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The customer or Plan doesn't exist")
    
    customer_plan_db = CustomerPlan(plan_id=plan_db.id, customer_id=customer_db.id, status=plan_status)
    session.add(customer_plan_db)
    session.commit()
    session.refresh(customer_plan_db)
    return customer_plan_db

@router.get("/customers/{customer_id}/plans", tags=['Customers'])
async def list_customer_plans(customer_id: int, session: SessionDep, plan_status: StatusEnum = Query()):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exist")
    
    query = select(CustomerPlan).where(CustomerPlan.customer_id == customer_id).where(CustomerPlan.status == plan_status)
    plans = session.exec(query).all()
    
    if len(plans) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The client has no purchased plans")
    
    return plans


    
    
    