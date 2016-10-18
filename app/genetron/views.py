from . import genetron
from flask import render_template
from flask import jsonify, request, g, url_for, current_app
from models import *

@genetron.route('/', methods=['GET', 'POST'])
@genetron.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('genetron/tables.html')

@genetron.route('/table')
def tables():
    data=Table.query.all()
    # return data
    return jsonify(
        data=[i.serialize for i in data ]
    )
#
#
# return jsonify({
#         'comments': [comment.to_json() for comment in comments],
#         'prev': prev,
#         'next': next,
#         'count': pagination.total
#     })

@genetron.route('/editortable')
def editortable():
    data=Table.query.all()
    return jsonify(
        data=[i.json for i in data ]
    )
@genetron.route('/editorhtml',methods=['GET', 'POST'])
def editorhtml():
    return render_template('genetron/editor_table.html')

@genetron.route('/editorresponse')
def editorresponse():
    return 'afds'