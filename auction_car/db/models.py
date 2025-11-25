from auction_car.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Enum, Date, DateTime, ForeignKey, Text
from typing import Optional, List
from enum import Enum as PyEnum
from datetime import datetime, date
from passlib.hash import bcrypt


class StatusChoices(str, PyEnum):
    seller ='seller'
    buyer ='buyer'


class UserProfile(Base):
    __tablename__ = 'user_profile'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[StatusChoices] = mapped_column(Enum(StatusChoices))
    phone_number: Mapped[Optional[str]] = mapped_column(String)
    car_owner: Mapped[List['Car']] = relationship('Car', back_populates='owner_car',
                                                  cascade='all, delete-orphan')
    buyer: Mapped[List["Bid"]] = relationship("Bid", back_populates='user',
                                        cascade='all, delete-orphan')
    feedback_seller: Mapped[List["Feedback"]] = relationship("Feedback", foreign_keys="[Feedback.seller_id]",
                                                             back_populates='seller',cascade='all, delete-orphan')
    feedback_buyer: Mapped[List["Feedback"]] = relationship("Feedback", foreign_keys="[Feedback.buyer_id]",
                                                            back_populates='buyer', cascade='all, delete-orphan')
    tokens: Mapped[List['RefreshToken']] = relationship('RefreshToken', back_populates='user',
                                                        cascade='all, delete-orphan')

    def set_passwords(self, password: str):
        self.password = bcrypt.hash(password)

    def check_password(self, password: str):
        return bcrypt.verify(password, self.password)

    def __str__(self):
        return f'{self.username}, {self.first_name}, {self.last_name}'


class RefreshToken(Base):
    __tablename__= 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow())
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    user: Mapped['UserProfile'] = relationship("UserProfile", back_populates='tokens')


class CheckFuel(str, PyEnum):
    petrol ='petrol'
    diesel ='diesel'
    gas = 'gas'
    electro = 'electro'


class CheckCar(str, PyEnum):
    auto = 'auto'
    manual = 'manual'


class Car(Base):
    __tablename__ = 'car'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    brand: Mapped[str] = mapped_column(String)
    model: Mapped[str] = mapped_column(String)
    year: Mapped[date] = mapped_column(Date)
    fuel_type: Mapped[CheckFuel] = mapped_column(Enum(CheckFuel))
    transmission: Mapped[CheckCar] = mapped_column(Enum(CheckCar))
    milage: Mapped[int] = mapped_column(Integer)
    price: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    images: Mapped[str] = mapped_column(String)
    seller_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    owner_car: Mapped['UserProfile'] = relationship('UserProfile',  back_populates='car_owner')
    auction: Mapped[List['Auction']] = relationship('Auction', back_populates='car',
                                              cascade='all, delete-orphan')


class Status(str, PyEnum):
    active = 'active'
    completed = 'completed'
    canceled = 'canceled'


class Auction(Base):
    __tablename__ = "auction"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    car_id: Mapped[int] = mapped_column(Integer, ForeignKey('car.id'), unique=True)
    car: Mapped['Car'] = relationship('Car', back_populates='auction')
    start_price: Mapped[int] = mapped_column(Integer, default=0)
    min_price: Mapped[int] = mapped_column(Integer, nullable=True)
    start_time: Mapped[datetime] = mapped_column(DateTime)
    end_time: Mapped[datetime] = mapped_column(DateTime)
    status:  Mapped[Status] = mapped_column(Enum(Status))
    bid: Mapped[List["Bid"]] = relationship("Bid", back_populates="auction",
                                      cascade="all, delete-orphan")


class Bid(Base):
    __tablename__ = "bid"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    auction_id: Mapped[int] = mapped_column(ForeignKey('auction.id'))
    auction: Mapped['Auction'] = relationship('Auction', back_populates='bid')
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='buyer')
    amount: Mapped[int] = mapped_column(Integer)
    created_date: Mapped[datetime] = mapped_column(DateTime)


class Feedback(Base):
    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    seller_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    seller: Mapped['UserProfile'] = relationship('UserProfile', back_populates='feedback_seller',
                                                 foreign_keys=[seller_id])
    buyer_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    buyer: Mapped['UserProfile'] = relationship('UserProfile', back_populates='feedback_buyer',
                                                foreign_keys=[buyer_id])
    rating: Mapped[int] = mapped_column(Integer)
    text: Mapped[str] = mapped_column(Text)
    created_date: Mapped[datetime] = mapped_column(DateTime,default=datetime.utcnow())

