from typing import List
from auction_car.db.models import Bid
from auction_car.db.schema import BidCreateSchema, BiOutSchema
from fastapi import APIRouter, Depends, HTTPException
from auction_car.db.database import SessionLocal
from sqlalchemy.orm import Session

bid_router = APIRouter(prefix='/bid', tags=['Bid'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@bid_router.post("/create", response_model=BidCreateSchema)
async def bid_create(task: BidCreateSchema, db: Session = Depends(get_db)):
    bid_db = Bid(**task.dict())
    db.add(bid_db)
    db.commit()
    db.refresh(bid_db)
    return bid_db


@bid_router.get('/', response_model=List[BiOutSchema])
async def bid_list(db: Session = Depends(get_db)):
    return db.query(Bid).all()


@bid_router.get('/{bid_id}', response_model=BiOutSchema)
async def bid_detail(bid_id: int, db: Session = Depends(get_db)):
    bid = db.query(Bid).filter(Bid.id == bid_id).first()

    if bid is None:
        raise HTTPException(status_code=400, detail='Мындай маалымат жок')
    return bid


@bid_router.delete('/{car_id}')
async def bid_delete(bid_id: int, db: Session = Depends(get_db)):
    bid_db = db.query(Bid).filter(Bid.id == bid_id).first()

    if bid_db is None:
        raise HTTPException(status_code=400, detail='Мындай маалымат жок')

    db.delete(bid_db)
    db.commit()
    return {"message": "This is deleted"}
