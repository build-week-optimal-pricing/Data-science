#!/usr/bin/env python3

from api import DB
from api.models.listing import Listing


def get_all_queries():
    """
        Returns all stored listing queries.
    """
    return list(Listing.query.all())
