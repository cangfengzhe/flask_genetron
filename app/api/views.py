
from flask import Flask, Blueprint
from flask_restful import Api, Resource, url_for
from . import api



class TodoItem(Resource):
    def get(self, id):
        return {'task': 'Say "Hello, World!"'}

api.add_resource(TodoItem, '/todos/<int:id>')


# class HelloWorld(restful.Resource):
#     def get(self):
#         return {'hello': 'world'}

# api.add_resource(HelloWorld, '/')

# api.init_app(app)

class SnpIndel(Resource):
    def get(self,id):
        pass