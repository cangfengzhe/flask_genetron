#coding=utf-8
from .. import db


class Patient(db.Model):
    __tablename__ = 'patient'
    SEX = [
        (u'M', u'男'),
        (u'F', u'女')
    ]
    id = db.Column(db.Integer, primary_key=True)
    patient_id=db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(120))
    age = db.Column(db.Integer)
    sex = db.Column(db.String(10))
    hospital = db.Column(db.String(30))
    histology = db.Column(db.String(100))
    # addr= db.Column(db.String(50))
    tissue=db.Column(db.String(150))
    indication=db.Column(db.String(150))
    panel=db.Column(db.String(20))
    bioinfo=db.Column(db.Boolean, default=False)
    bioinfo_time = db.Column(db.DateTime)

    ask_histology_time = db.Column(db.DateTime)
    get_histology_time = db.Column(db.DateTime)
    ask_histology = db.Column(db.Boolean, default=False)
#
    start_time=db.Column(db.Date)
    dead_line=db.Column(db.Date)
    is_finish=db.Column(db.Boolean, default=False)
    is_finish_time = db.Column(db.DateTime)
    note=db.Column(db.Text)

    def __init__(self, **kwargs):
        super(Patient, self).__init__(**kwargs)
        if kwargs:
            self.from_dict(kwargs)

    def proc_time(self, time_var, time_fmt = "%Y-%m-%d %H:%M:%S"):
        if time_var:
            return time_var.strftime(time_fmt)
        else:
            return ''

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return [self.patient_id,
               self.name,
               self.age,
               self.sex,
               self.hospital,
               self.histology,
               self.tissue,
               self.indication,
               self.panel,
               self.bioinfo,
               self.start_time,
               self.dead_line,
               self.note]

    @property
    def json(self):
        return {'DT_RowId' : self.id,
               'patient_id' : self.patient_id,
               'name' : self.name,
               'age' : self.age,
               'sex' : self.sex,
               'hospital' : self.hospital,
               'histology':self.histology,
               'tissue' : self.tissue,
               'indication' : self.indication,
               'panel': self.panel,
               'bioinfo': self.bioinfo,
               'bioinfo_time': self.proc_time(self.bioinfo_time, "%Y-%m-%d %H:%M:%S"),
                'ask_histology': self.ask_histology,
                'ask_histology_time': self.proc_time(self.ask_histology_time, "%Y-%m-%d %H:%M:%S"),
                'get_histology_time': self.proc_time(self.get_histology_time, "%Y-%m-%d %H:%M:%S"),
                'is_finish': self.is_finish,
                'is_finish_time': self.proc_time(self.is_finish_time, "%Y-%m-%d %H:%M:%S"),
               'start_time' : self.proc_time(self.start_time, "%Y-%m-%d"),
               'dead_line' : self.dead_line.strftime("%Y-%m-%d"),
               'note' : self.note
               }

    def from_dict(self, dick_data):
        for (k, w) in dick_data.items():
            setattr(self, k, w)

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
