#!/usr/bin/env python3

import logging

from decouple import config
from dotenv import load_dotenv

from flask import Flask 
from dash import Dash

APP = Flask(__name__)
DASH = Dash(__name__, server=APP)
LOG = logging.getLogger("optimal-price")
logging.basicConfig(level=logging.DEBUG)

from api import routes
