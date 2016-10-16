
from app import create_app, db

import os
from  app.genetron.models import Table



app = create_app('development')
app_context = app.app_context()
app_context.push()
db.create_all()
for ii in range(100):
    aa=Table(name='name'+str(ii), age=ii)
    db.session.add(aa)
db.session.commit()


print('hafsd')
