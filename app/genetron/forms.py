#coding=utf-8
from flask_wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, HiddenField, SelectField,\
    SubmitField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from flask_login import login_required, current_user
from wtforms.validators import DataRequired
from .models import Doc_type


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
    
    
class DocumentForm(Form):
    title = StringField('title', validators=[DataRequired()])
    doc_type_id = SelectField('type', coerce=int)
    body = PageDownField("content", validators=[Required()])
    submit = SubmitField('Submit')
    
    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        self.doc_type_id.choices = [(doc_type.id, doc_type.type_name)
                             for doc_type in Doc_type.query.all()]

        
class EditDocumentForm(Form):
    title = StringField('title', validators=[DataRequired()])
    doc_type_id = SelectField('type', coerce=int)
    body = PageDownField("content", validators=[Required()])
    submit = SubmitField('Submit')
    
    def __init__(self, *args, **kwargs):
        super(EditDocumentForm, self).__init__(*args, **kwargs)
        self.doc_type_id.choices = [(doc_type.id, doc_type.type_name)
                             for doc_type in Doc_type.query.all()]   