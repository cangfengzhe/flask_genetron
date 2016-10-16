import os
from flask import Flask, url_for, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from wtforms import form, fields, validators
#import flask_admin as admin
import flask_login as login
from flask_admin.contrib import sqla
from flask_admin import helpers, expose
from werkzeug.security import generate_password_hash, check_password_hash


class MyModelView(sqla.ModelView):
    inline_models = ['Role', ]
    # def is_accessible(self):
    #     return login.current_user.is_authenticated
    def is_accessible(self):
        return True

