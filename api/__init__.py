#!/usr/bin/env python3

import logging

from decouple import config
from dotenv import load_dotenv
import dash_html_components as html
import dash_core_components as dcc

from flask import Flask 
from dash import Dash

APP = Flask(__name__)

DASH = Dash(
    __name__,
    server=APP,
    external_stylesheets=[
        "/css/style.css",
    ],
    url_base_pathname="/plot/",
)
DASH.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        dcc.Graph(id="main-graph", style={"height": "100%", "width": "100%"}),
    ],
    id="page-content",
    style={"height": "100%", "width": "100%"},
)
#DASH.config.suppress_callback_exceptions = True

LOG = logging.getLogger("optimal-price")
logging.basicConfig(level=logging.DEBUG)

from api import routes
