#!/usr/bin/env python3

from api import DB

class Listing(DB.Model):
    """
        Database table for listings.
    """
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    neighborhood = DB.Column(DB.Unicode(30), nullable=False)
    room_type = DB.Column(DB.Unicode(20), nullable=False)
    min_nights = DB.Column(DB.Integer, nullable=True)
    num_reviews = DB.Column(DB.Integer, nullable=True)
    listings_count = DB.Column(DB.Integer, nullable=True)
    availability_365 = DB.Column(DB.Integer, nullable=True)
    last_review = DB.Column(DB.Integer, nullable=True)
    price = DB.Column(DB.Float, nullable=False)
