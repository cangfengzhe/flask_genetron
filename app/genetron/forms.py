#coding=utf-8
from flask_wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, HiddenField, SelectField,\
    SubmitField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField

from wtforms.validators import DataRequired



class CheckForm(Form):
    id = HiddenField('id')
    flowcell = StringField('flowcell', validators=[DataRequired()])
    panel = StringField('panel', validators=[DataRequired()])
    check_type = StringField('check_type', validators=[DataRequired()])
    gene_info = StringField('gene')
    start_time = StringField('start_time', validators=[DataRequired()])
    end_time = StringField('end_time')
    result = StringField('result')
    note = StringField('note')
    