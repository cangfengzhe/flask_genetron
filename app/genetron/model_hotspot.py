#coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import datetime

from markdown import markdown
import bleach
import  sqlalchemy

from .. import db
from app.utils import *


class Gene_info(db.Model):
    __tablename__='hotspot_gene_info'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    
    flowcell_id = db.Column(db.Integer, db.ForeignKey('flowcell_info.id'))
    panel=db.Column(db.String(200))
    sample_time =  db.relationship('Sample_time_info', backref='sample_flowcell_id', lazy="dynamic")
    sample_flowcell_info =  db.relationship('Sample_flowcell_info', backref='sample_flowcell_id', lazy="dynamic")