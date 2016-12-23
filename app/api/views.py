#coding=utf-8
import json

from flask import Flask, Blueprint, jsonify
from flask_restful import Api, Resource, url_for
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
    
api.add_resource(SnpIndel, '/snpindel/<string:id>')
        
    
class Cnv(Resource):
    def get(self,id):
        sample = Sample_info.query.filter_by(sample_id=id).first()
        if sample:
            cnv_info = sample.cnv_info
            return jsonify(data=[xx.json for xx in cnv_info])
        else:
            return jsonify(data='error')
        
api.add_resource(Cnv, '/cnv/<string:id>')       
        