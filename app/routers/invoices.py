import os
from typing import Annotated
from dotenv import load_dotenv
from fastapi import HTTPException, security, status, APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from models import Invoice

router = APIRouter()
security = HTTPBasic()
load_dotenv()

user = os.getenv("USER")
password = os.getenv("PASSWORD")

@router.post("/invoices", tags=['Invoices'])
async def create_invoice(invoice_data: Invoice,
                         credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    
    if credentials.username == user and credentials.password == password:
        return invoice_data
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user")