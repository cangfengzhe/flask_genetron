#coding=utf-8
import json

from flask import Flask, Blueprint, jsonify
from flask_restful import Api, Resource, url_for, reqparse
from . import api
from ..genetron.models import *




class SnpIndel(Resource):
    def get(self,id):
        sample = Sample_info.query.filter_by(sample_id=id).first()
        if sample:
            snp_indel_info = sample.snp_indel_info
            return jsonify(data=[xx.json for xx in snp_indel_info])
        else:
            return jsonify(data='error')
    
api.add_resource(SnpIndel, '/snpindel/<string:id>', endpoint='snpindel')
        
    
class Cnv(Resource):
    def get(self,id):
        sample = Sample_info.query.filter_by(sample_id=id).first()
        if sample:
            cnv_info = sample.cnv_info
            return jsonify(data=[xx.json for xx in cnv_info])
        else:
            return jsonify(data='error')
    def put(self, id):
        return {'aa':'bb'}

    def delete(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('age', type=int, help='Rate cannot be converted')
        parser.add_argument('panel')
        args = parser.parse_args()
        return {'type':[args.age, args.panel]}
        
api.add_resource(Cnv, '/cnv/<string:id>', endpoint='cnv')


        