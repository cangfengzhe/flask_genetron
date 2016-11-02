
from app import create_app, db

import os
import datetime
from  app.genetron.models import Table, Patient


app = create_app('development')
app_context = app.app_context()
app_context.push()
db.create_all()
for ii in range(100):
    # aa=Table(name='name'+str(ii), age=ii)
    bb = {'patient_id':'PA0'+str(ii), 'name':'fad', 'age':101, 'tissue':'tissue', 'indication':'cancer',
          'start_time':datetime.datetime.strptime('2016-11-01', '%Y-%m-%d').date(),
          'dead_line': datetime.datetime.strptime('2016-11-01', '%Y-%m-%d').date()}
    patient=Patient(**bb)
    # db.session.add(aa)
    db.session.add(patient)
db.session.commit()


print('hafsd')
