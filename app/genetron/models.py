from .. import db
from datetime import datetime

class Table(db.Model):
    __tablename__ = 'table'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    age = db.Column(db.Integer)
    # addr= db.Column(db.String(50))

    def __init__(self, name, age):
        self.name = name
        self.age = age

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return [self.name,
        self.age]
    @property
    def json(self):

        return {'id':self.id,
               'first_name':self.name,
               'last_name':self.name
               }

class Patient(db.Model):
    __tablename__ = 'patient'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    age = db.Column(db.Integer)
    # addr= db.Column(db.String(50))
    tissue=db.Column(db.String(150))
    cancer=db.Column(db.String(150))
    start_time=db.Column(db.DateTime)
    finish_time=db.Column(db.DateTime)
    # project=db.relationship(Project, )
    def __init__(self, patient_id, name, age, tissue, cancer, start_time=None, finish_time=None):
        self.patient_id=patient_id
        self.name=name
        self.age=age
        self.tissue=tissue
        self.cancer=cancer
        self.start_time=start_time
        self.finish_time=finish_time
    def __repr__(self):
        return self.name

# class Project(db.Model):

#
class Project(db.Model):
    __tablename__='project'
    id = db.Column(db.Integer, primary_key=True)
    patient_id=db.Column(db.Integer,db.ForeignKey('patient.id'))
    patient = db.relationship('Patient',
        backref=db.backref('project', lazy='dynamic'))
    t_samp=db.Column(db.String(20))
#
#     def __init__(self):
#         self
    def __repr__(self):
        return self.t_samp

class EditorTable(db.Model):
    __tablename__='editortable'
    id = db.Column(db.Integer, primary_key=True)
    first_name=db.Column(db.String(20))
    last_name=db.Column(db.String(20))
    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {'id':self.id,
               'first_name':self.first_name,
               'last_name':self.last_name
               }



#
# class Role(db.Model):
#     __tablename__ = 'roles'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True)
#     default = db.Column(db.Boolean, default=False, index=True)
#     permissions = db.Column(db.Integer)
#     users = db.relationship('User', backref='role', lazy='dynamic')
