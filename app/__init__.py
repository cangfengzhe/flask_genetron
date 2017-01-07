from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
from config import config
from flask_admin import Admin
from flask_restful import Api


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()
# api = Api()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

from admin.app import MyModelView, ProjectView
from genetron.models import *
import sqlalchemy

def datetimeformat(value, format="%Y-%m"):
    if value:
        return value.strftime(format)
    else:
        return ''

def get_item_time(flowcell, item_type):
    flag = flowcell.sample_time.filter_by(item_type=item_type).first()
    if flag:
        return flag.item_time.strftime("%Y-%m-%d %H:%M:%S")
    else:
        return ''
    
def create_app(config_name):
    app = Flask(__name__)
    
    #jinja2
    app.jinja_env.filters['datetimeformat'] = datetimeformat
    app.jinja_env.filters['get_item_time'] = get_item_time
    app.jinja_env.globals['sqlalchemy'] = sqlalchemy# Sample_time_info
    app.jinja_env.globals['Sample_time_info'] = Sample_time_info
    # jinja2.Environment(extensions=["jinja2.ext.do",])
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    # from flask.ext import restful
    
    # api.init_app(app)
    from .models import User,Role
    # from genetron.models import *
    admin=Admin()
    admin.add_view(MyModelView(User, db.session))
    admin.add_view(MyModelView(Role, db.session))
    admin.add_view(MyModelView(Biomarker, db.session))
    # admin.add_view(ProjectView(Project, db.session))
    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask_sslify import SSLify
        sslify = SSLify(app)


    from .genetron import genetron as genetron_blueprint
    app.register_blueprint(genetron_blueprint, url_prefix='/genetron')
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')
    
    from .api import restful_api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    
    
    return app
