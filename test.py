
from app import create_app, db

import os
from  app.genetron.models import Table, Patient


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


print('hafsd')
