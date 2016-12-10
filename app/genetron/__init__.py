from flask import Blueprint

genetron = Blueprint('genetron', __name__)

from . import views
from . import views2

from ..models import Permission


@genetron.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)