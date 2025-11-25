from auction_car.db.models import *
from sqladmin import ModelView


class CarAdmin(ModelView, model=Car):
    column_list = [Car.id]


class BidAdmin(ModelView, model=Bid):
    column_list = [Bid.id]


class FeedbackAdmin(ModelView, model=Feedback):
    column_list = [Feedback.id]


class AuctionAdmin(ModelView, model=Auction):
    column_list = [Auction.id]
