#!/usr/bin/env python3

import logging
from flask import request, jsonify, render_template
import numpy as np

from api import APP
from api.service import location_service
from api.service import price_service

LOG = logging.getLogger("optimal-price")

@APP.route("/lookup-neighborhood", methods=["GET", "POST"])
def lookup_neighborhood():
    """
        Endpoint for looking up a neighborhood from a pair of coordinates.

        Expects "latitude" and "longitude" URL parameters as floats.

        Returns a json object containing the neighborhood.
    """

    if request.method == "GET":
        lat = float(request.args.get("latitude"))
        long = float(request.args.get("longitude"))

    elif request.method == "POST":
        lat = float(request.form["latitude"])
        long = float(request.form["longitude"])

    result = location_service.get_neighborhood(lat, long)
    
    return jsonify({
        "neighborhood": result
    })

@APP.route("/lookup-neighborhood-form")
def lookup_neighborhood_form():
    return render_template("coords-form.html")


@APP.route("/estimate-price", methods=["POST"])
def estimate_price():
    """
        Endpoint for looking up price estimate given characteristics
        of the listing.
    """

    if "neighborhood" in request.form and "room_type" in request.form:
        data = request.form
    else:
        data = request.get_json()

    LOG.info(f"/estimate-price endpoint: got data: {data}")

    neighborhood = data["neighborhood"] 
    room_type = data["room_type"] 
    listings_count = (
       int(data["listings_count"])
       if "listings_count" in data else np.nan
    )
    num_reviews = (
       int(data["num_reviews"])
       if "num_reviews" in data else np.nan
    )
    min_nights = (
       int(data["min_nights"])
       if "min_nights" in data else np.nan
    )
    availability_365 = (
       int(data["availability"])
       if "availability" in data else np.nan
    )
    last_review_time = (
       int(data["last_review_time"])
       if "last_review_time" in data else np.nan
    )


    price = price_service.estimate(
       neighborhood=neighborhood,
       room_type=room_type,
       min_nights=min_nights,
       num_reviews=num_reviews,
       listings_count=listings_count,
       availability_365=availability_365,
       last_review=last_review_time,
    )


    return jsonify({
       "price": float(price)
    })

@APP.route("/estimate-price-form")
def estimate_price_form():
    return render_template("price-form.html")
