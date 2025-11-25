from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, date
from typing import Optional
from typing import List
from .models import StatusChoices, Status, CheckCar, CheckFuel


class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: StatusChoices
    phone_number: Optional[str]

    class Config:
        from_attributes = True


class UserUpdateSchema(BaseModel):
    username: str
    email: EmailStr
    password:str
    role: StatusChoices
    phone_number: Optional[str]

    class Config:
        from_attributes = True


class UserOutSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str
    role: StatusChoices
    phone_number: Optional[str]

    class Config:
        from_attributes = True


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class CarCreateSchema(BaseModel):
    brand: str
    model: str
    year: date
    fuel_type: CheckFuel
    milage: int
    transmission: CheckCar
    price: int
    description: str
    images: str
    seller_id: int

    class Config:
        from_attributes = True


class CarUpdateSchema(BaseModel):
    brand: str
    model: str
    year: date
    fuel_type: CheckFuel
    milage: int
    transmission: CheckCar
    price: int
    description: str
    images: str
    seller_id: int

    class Config:
        from_attributes = True


class CarOutSchema(BaseModel):
    id: int
    brand: str
    model: str
    year: date
    fuel_type: CheckFuel
    milage: int
    price: int
    description: str
    images: str
    seller_id: int

    class Config:
        from_attributes = True


class AuctionCreateSchema(BaseModel):
    car_id: int
    start_price: int
    min_price: int
    start_time: datetime
    end_time: datetime
    status: Status

    class Config:
        from_attributes = True


class AuctionUpdateSchema(BaseModel):
    start_price: int
    min_price: int
    start_time: datetime
    end_time: datetime
    status: Status

    class Config:
        from_attributes = True


class AuctionOutSchema(BaseModel):
    id: int
    car_id: int
    start_price: int
    min_price: int
    start_time: datetime
    end_time: datetime
    status: Status

    class Config:
        from_attributes = True


class BidCreateSchema(BaseModel):
    auction_id: int
    user_id: int
    amount: int
    created_date: datetime

    class Config:
        from_attributes = True


class BiOutSchema(BaseModel):
    id: int
    auction_id: int
    user_id: int
    amount: int
    created_date: datetime

    class Config:
        from_attributes = True


class FeedbackCreateSchema(BaseModel):
    seller_id: int
    buyer_id: int
    rating: int = Field(gt=1, lt=6)
    text: str
    created_date: datetime

    class Config:
        from_attributes = True


class FeedbackOutSchema(BaseModel):
    id: int
    seller_id: int
    buyer_id: int
    rating: int = Field(gt=1, lt=6)
    text: str
    created_date: datetime

    class Config:
        from_attributes = True
