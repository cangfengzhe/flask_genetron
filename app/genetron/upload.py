#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

from models import *
from . import genetron
from .configure import Configure as configure

@genetron.route('/upload', methods=['GET', 'POST'])
def upload_file():
    sample_id = request.args.get('sample')
    print(sample_id)
    print(request.method)
    print(request.files)
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        # print(file.filename)
        print(filename)
        # print(aa)
        file.save(os.path.join(configure.UPLOAD_FOLDER, filename))
        return ''


@genetron.route('/rmfile', methods=['GET', 'POST'])
def rm_file():
    sample_id = request.args.get('sample')
    print(sample_id)
    print(request.method)
    print(request.files)
    if request.method == 'POST':
        filename = request.form['fileNames']
        # print(file.filename)
        print(filename)
        filename_abs = os.path.join(configure.UPLOAD_FOLDER, filename)
        # print(aa)
        if os.path.exists(filename_abs):
            os.remove(filename_abs)
            return ''
        else:
            return 'file does not exists'


@genetron.route('/filelist', methods=['GET', 'POST'])
def file_list():
    sample_id = request.args.get('sample')
    file_list = [xx for xx in os.listdir(configure.UPLOAD_FOLDER)]
    # print(aa)
    return jsonify(data = file_list)