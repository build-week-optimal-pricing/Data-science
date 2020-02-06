#!/usr/bin/env python3

import logging
from io import BytesIO
import tarfile
import pickle
import numpy as np
import pandas as pd
import urllib.request

from api import DB
from api.models.listing import Listing


LOG = logging.getLogger("optimal-price")

def __loadModel():
    """
        Loads the model.
    """
    t = tarfile.open("pickles/pickles.tar.gz", "r:gz")
    with t.extractfile("pickles/primitive_model.pickle") as mf:
        model = pickle.load(mf)

    return model


_model = __loadModel()


def estimate(
       neighborhood="",
       room_type="",
       min_nights=0,
       num_reviews=0,
       listings_count=0,
       availability_365=0,
       last_review=0,
):
    """
        Service for doing price estimate.

        @type neighborhood: str
        @type room_type: str
        @type min_nights: int
        @type num_reviews: int
        @type listings_count: int
        @type availability_365: int
        @type last_review: int

        @rtype: float
    """

    if min_nights is np.nan:
        LOG.info("Warning: min_nights is nan")

    if num_reviews is np.nan:
        LOG.info("Warning: num_reviews is nan")

    if listings_count is np.nan:
        LOG.info("Warning: listings_count is nan")

    if availability_365 is np.nan:
        LOG.info("Warning: availability_365 is nan")

    if last_review is np.nan:
        LOG.info("Warning: last_review is nan")

    df = pd.DataFrame({
        'neighbourhood_group': [neighborhood],
        'room_type': [room_type],
        'minimum_nights': [min_nights],
        'number_of_reviews': [num_reviews],
        'reviews_per_month': [np.nan], # TODO
        'calculated_host_listings_count': [listings_count],
        'availability_365': [availability_365],
        'last_review_seconds_ago': [last_review],
    })

    pred = _model.predict(df)
    # we don't want to recommend less than 5 (arbitrary)
    price = float(pred[0]) if pred[0] > 5. else 5.

    listing = Listing(
        neighborhood=neighborhood,
        room_type=room_type,
        min_nights=min_nights if min_nights is not np.nan else None,
        num_reviews=num_reviews if num_reviews is not np.nan else None,
        listings_count=listings_count if listings_count is not np.nan else None,
        availability_365=availability_365 if availability_365 is not np.nan else None,
        last_review=last_review if last_review is not np.nan else None,
        price=price,
    )

    DB.session.add(listing)
    DB.session.commit()

    return price
