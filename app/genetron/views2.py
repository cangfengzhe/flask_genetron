#coding=utf-8

from flask import jsonify, request
from flask import render_template
from collections import defaultdict
from models import *
from . import genetron
from flask_login import login_required
import sqlalchemy
import datetime
# from ..models import User


@genetron.route('/msg')
def msg():
    return render_template('msg.html')

@genetron.route('/msg_response')
def msg_response():
    user = request.args.get('user')
    from ..models import User
    user_id = User.query.filter_by(username=user).first().id
    info = Send_info.query.filter_by(receive_user_id=user_id, read=False)
    info_count = info.count()

    return jsonify(data= [xx.json() for xx in info if xx])

@genetron.route('/igv')
def igv():
    return render_template('genetron/igv.html')
    
    



