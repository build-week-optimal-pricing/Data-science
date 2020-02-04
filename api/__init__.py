#!/usr/bin/env python3

import logging

from decouple import config
from dotenv import load_dotenv
import dash_html_components as html
import dash_core_components as dcc

from flask import Flask 
from dash import Dash

APP = Flask(__name__)

"""
DASH = Dash(
    __name__,
    server=APP,
    routes_pathname_prefix="/vis/",
)
DASH.layout = html.Div([], id="page-content")
DASH.config.suppress_callback_exceptions = True
"""

LOG = logging.getLogger("optimal-price")
logging.basicConfig(level=logging.DEBUG)

from api import routes
