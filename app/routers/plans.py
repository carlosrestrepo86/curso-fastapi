import os
from typing import Annotated
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status, security
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlmodel import select
from db import SessionDep
from models import Plan

router = APIRouter()
security = HTTPBasic()
load_dotenv()

user = os.getenv("USER")
password = os.getenv("PASSWORD")

@router.post("/plans", status_code=status.HTTP_201_CREATED, tags=["Plans"])
async def create_plan(plan_data: Plan,
                      session: SessionDep,
                      credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    
    if credentials.username == user and credentials.password == password:
        plan_db = Plan.model_validate(plan_data.model_dump())
        session.add(plan_db)
        session.commit()
        session.refresh(plan_db)
        return plan_db
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user")
    
@router.get("/plans", response_model=list[Plan], tags=["Plans"])
async def list_plan(session: SessionDep):
    plans = session.exec(select(Plan)).all()
    return plans
 