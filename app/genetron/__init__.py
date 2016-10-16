from flask import Blueprint

genetron = Blueprint('genetron', __name__)

from . import views
