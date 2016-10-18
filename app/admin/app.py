import os
from flask import Flask, url_for, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from wtforms import form, fields, validators
#import flask_admin as admin
import flask_login as login
from flask_admin.contrib import sqla
from flask.ext.admin.form import Select2Widget
from flask_admin import helpers, expose
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import User, Role

class MyModelView(sqla.ModelView):

    # inline_models = ['Role']
    column_hide_backrefs = False
    # form_extra_fields = {
    #     'role': sqla.fields.QuerySelectField(
    #         label='name',
    #         query_factory=lambda: Role.query.all,
    #         widget=Select2Widget()
    #     )
    # }
    # column_list = ('email', 'username', 'role')
    # def is_accessible(self):
    #     return login.current_user.is_authenticated
    def is_accessible(self):
        return True



class ProjectView(sqla.ModelView):

    # inline_models = ['Role']
    column_list = ['patient_id', 'patient.name', 'patient.age']
    column_hide_backrefs = False
    # form_extra_fields = {
    #     'role': sqla.fields.QuerySelectField(
    #         label='name',
    #         query_factory=lambda: Role.query.all,
    #         widget=Select2Widget()
    #     )
    # }
    # column_list = ('email', 'username', 'role')
    # def is_accessible(self):
    #     return login.current_user.is_authenticated
    def is_accessible(self):
        return True