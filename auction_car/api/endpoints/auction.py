from typing import List
from auction_car.db.models import Auction
from auction_car.db.schema import AuctionCreateSchema, AuctionUpdateSchema, AuctionOutSchema
from fastapi import APIRouter, Depends, HTTPException
from auction_car.db.database import SessionLocal
from sqlalchemy.orm import Session

auction_router = APIRouter(prefix='/auction', tags=['Auction'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@auction_router.post("/create", response_model=AuctionCreateSchema)
async def auction_create(auction: AuctionCreateSchema, db: Session = Depends(get_db)):
    auction_db = Auction(**auction.dict())
    db.add(auction_db)
    db.commit()
    db.refresh(auction_db)
    return auction_db


@auction_router.get('/', response_model=List[AuctionOutSchema])
async def auction_list(db: Session = Depends(get_db)):
    return db.query(Auction).all()


@auction_router.get('/{auction_id}', response_model=AuctionOutSchema)
async def auction_detail(auction_id: int, db: Session = Depends(get_db)):
    auction = db.query(Auction).filter(Auction.id == auction_id).first()

    if auction is None:
        raise HTTPException(status_code=400, detail='Мындай маалымат жок')
    return auction


@auction_router.put('/{auction_id}', response_model=AuctionUpdateSchema)
async def auction_update(auction_id: int, auction: AuctionUpdateSchema, db: Session = Depends(get_db)):
    auction_db = db.query(Auction).filter(Auction.id == auction_id).first()

    if auction_db is None:
        raise HTTPException(status_code=400, detail='Мындай маалымат жок')


    for auction_key, auction_values in auction.dict().items():
        setattr(auction_db, auction_key, auction_values)

    db.add(auction_db)
    db.commit()
    db.refresh(auction_db)
    return auction_db


@auction_router.delete('/{auction_id}')
async def auction_delete(auction_id: int, db: Session = Depends(get_db)):
    auction_db = db.query(Auction).filter(Auction.id == auction_id).first()

    if auction_db is None:
        raise HTTPException(status_code=400, detail='Мындай маалымат жок')

    db.delete(auction_db)
    db.commit()
    return {"message": "This is deleted"}
