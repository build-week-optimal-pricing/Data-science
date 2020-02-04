#!/usr/bin/env python3

from io import BytesIO
import tarfile
import pickle
import numpy as np
import pandas as pd
import urllib.request


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
    df = pd.DataFrame({
        'neighbourhood_group': [neighborhood],
        'room_type': [room_type],
        'minimum_nights': [min_nights],
        'number_of_reviews': [num_reviews],
        'reviews_per_month': [num_reviews/3], # TODO 
        'calculated_host_listings_count': [listings_count],
        'availability_365': [availability_365],
        'last_review_seconds_ago': [last_review],
    })

    pred = _model.predict(df)
    return pred[0]
