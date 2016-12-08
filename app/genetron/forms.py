#coding=utf-8
from flask_wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from ..models import Role, User


class Report_from(Form):
     report_user = SelectField(u'报告完成', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])