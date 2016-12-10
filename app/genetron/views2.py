#coding=utf-8

from flask import jsonify, request
from flask import render_template
from collections import defaultdict
from models import *
from . import genetron
from flask_login import login_required
import sqlalchemy
import datetime


@genetron.route('/sample_table2')
def sample_table2():
    data = Sample_info.query.filter(Sample_info.sample_id.like('%T%') |  Sample_info.panel.like('%ctDNA%'))
    return jsonify(
        [i.json for i in data if i.patient]
    )