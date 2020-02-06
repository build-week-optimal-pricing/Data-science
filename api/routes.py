#!/usr/bin/env python3

import logging
from flask import request, jsonify, render_template, send_from_directory
import numpy as np
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

from api import APP, DASH
from api.service import location_service
from api.service import listing_service
from api.service import price_service
from api.service import plot_service


LOG = logging.getLogger("optimal-price")


@DASH.callback(
    Output("main-graph", "figure"),
    [Input("url", "pathname"),],
)
def get_visualization(pathname):
    LOG.info(f"get_visualization('{pathname}')")

    path_components = pathname.split("/")
    assert len(path_components) == 3
    assert path_components[0] == ""
    assert path_components[1] == "plot"

    if path_components[-1] == "random":
        return plot_service.random_plot()

    if path_components[-1] == "map":
        return plot_service.map_plot()

    if path_components[-1] == "scatter":
        return plot_service.scatter_plot()

    # shouldn't get here
    assert False


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
       if "listings_count" in data and data["listings_count"] else np.nan
    )
    num_reviews = (
       int(data["num_reviews"])
       if "num_reviews" in data and data["num_reviews"] else np.nan
    )
    min_nights = (
       int(data["min_nights"])
       if "min_nights" in data and data["min_nights"] else np.nan
    )
    availability_365 = (
       int(data["availability"])
       if "availability" in data and data["availability"] else np.nan
    )
    last_review_time = (
       int(data["last_review_time"])
       if "last_review_time" in data and data["last_review_time"] else np.nan
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

@APP.route("/lookup-neighborhood-form")
def lookup_neighborhood_form():
    return render_template("coords-form.html")

@APP.route("/view-queries")
def view_queries():
    listings = listing_service.get_all_queries()
    return render_template("listings.html", listings=listings)


@APP.route("/css/<filename>")
def get_css(filename):
    LOG.info(f"get_css('{filename}')")
    return send_from_directory("../css", filename)
