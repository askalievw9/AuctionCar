from fastapi import FastAPI
from sqladmin import Admin
from .views import *
from auction_car.db.models import *
from auction_car.db.database import engine


def setup_admin(app: FastAPI):
    admin = Admin(app, engine)
    admin.add_view(CarAdmin)
    admin.add_view(BidAdmin)
    admin.add_view(FeedbackAdmin)
    admin.add_view(AuctionAdmin)
