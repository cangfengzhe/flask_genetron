#coding=utf-8
#!/usr/bin/env python3
# Project: flask_genetron
# Filename: import_db.py
# Description: 
# Author: Li Pidong
# E-mail: hope-dream@163.com
# Created: 22/10/16 20:25 
# Version:
# Last-Updated:

from app import create_app, db

import os
from  app.genetron.models import Table, Patient
import pandas as pd


app = create_app('development')
app_context = app.app_context()
app_context.push()
db.create_all()
# for ii in range(100):
#     aa=Table(name='name'+str(ii), age=ii)
#     patient=Patient(patient_id='PA0'+str(ii), name='fad', age=11, tissue='tissue', cancer='cancer', start_time=None, finish_time=None)
#     db.session.add(aa)
#     db.session.add(patient)
# db.session.commit()
info_data=pd.read_excel(u'/Users/lipidong/Downloads/项目进展1021.xlsx')
import numpy as np
def proc_nan(_value):
    try:
        if np.isnan(_value):
            return None
    except:
        return _value

for ii in range(10):
    info = info_data.iloc[ii, :]
    patient_id = info[0]
    name = info[1]
    sex = proc_nan(info[2])
    age = proc_nan(info[3])
    histology = proc_nan(info[4])
    indication = proc_nan(info[5])
    tissue = proc_nan(info[6])
    panel = proc_nan(info[8])
    start_time = info[9].date()
    dead_line = info[10].date()
    process = proc_nan(info[11])
    hospital=None
    note = None
    bioinfo=False
    pt=Patient(patient_id, name, age, sex, hospital, panel,bioinfo,  histology, tissue, indication, start_time, dead_line,process, note)
    db.session.add(pt)
db.session.commit()