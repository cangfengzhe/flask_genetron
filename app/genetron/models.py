from .. import db

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
       return [

            self.name,
           # This is an example how to deal with Many2Many relations
           self.age
       ]




# class Role(db.Model):
#     __tablename__ = 'roles'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True)
#     default = db.Column(db.Boolean, default=False, index=True)
#     permissions = db.Column(db.Integer)
#     users = db.relationship('User', backref='role', lazy='dynamic')
