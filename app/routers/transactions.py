from sqlmodel import func, select
from db import SessionDep
from models import Customer, Transaction, TransactionCreate
from fastapi import APIRouter, HTTPException, Query, status

router = APIRouter()

@router.post("/transactions",status_code=status.HTTP_201_CREATED, tags=['Transactions'])
async def create_transaction(transaction_data: TransactionCreate, session: SessionDep):
    transaction_data_dict = transaction_data.model_dump()
    customer = session.get(Customer, transaction_data_dict.get('customer_id'))
    if not customer: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exist")
    
    transaction_db = Transaction.model_validate(transaction_data_dict)
    session.add(transaction_db)
    session.commit()
    session.refresh(transaction_db)
    
    return transaction_db

@router.get("/transactions", tags=["Transactions"])
async def list_transactions(session: SessionDep,
                            offset: int = Query(0, description="Records to skip"),
                            limit: int = Query(10, description="Number of records")):
    
    # Total de registros
    # total_query = select(func.count()).select_from(Transaction)
    total_registers = len(session.exec(select(Transaction)).all())
    
    total_pages = (total_registers + limit - 1) // limit
    
    query = select(Transaction).offset(offset).limit(limit)
    transactions = session.exec(query).all()
    
    answer = {
        "data": transactions,
        "number of pages": total_pages,
        "elements per page": limit
    }
    
    return answer