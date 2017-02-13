from flask import Blueprint
from flask_restful import Api

restful_api = Blueprint('restful_api', __name__)
api = Api()
api.init_app(restful_api)

from . import views
