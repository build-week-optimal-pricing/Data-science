#!/usr/bin/env python3

import logging

from decouple import config
from dotenv import load_dotenv
import dash_html_components as html
import dash_core_components as dcc

from flask import Flask 
from dash import Dash
from flask_sqlalchemy import SQLAlchemy

# initialize flask app
APP = Flask(__name__)
APP.config["SQLALCHEMY_DATABASE_URI"] = config("DATABASE_URL")

# initialize dash, for visualizations
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

# initialize db
DB = SQLAlchemy(APP)

# initialize logging
LOG = logging.getLogger("optimal-price")
logging.basicConfig(level=logging.DEBUG)

from api import routes
