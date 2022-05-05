from flask import Blueprint
routes = Blueprint('routes', __name__)

from .categories import *
from .questions import *
from .errors_handling import *