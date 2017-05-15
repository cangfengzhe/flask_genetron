# coding=utf-8


import os
import datetime



from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from sqlalchemy import text
from json import dumps

from . import api
from app.genetron.configure import Configure as configure
from app.models import *
from app.genetron.models import *
from .. import app_dir
from app.utils import *
from flask_login import current_user
from app.email import send_email2

class Cnv_Email(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('sample', type=str)
        parser.add_argument('gene', type=str)
        parser.add_argument('panel', type=str)
        parser.add_argument('user', type=str)
        # parser.add_argument('callback',parser.add_argument('gene', type=str) type=str, help='note')
        args = parser.parse_args()
        user = args.user
        gene = args.gene
        panel = args.panel
        sample_id = args.sample
        sample = Sample_info.query.filter_by(sample_id=sample_id).first()
        days = configure.panel_period
        
        if panel in ['wes', 'WES', 'exome']:
            days = configure.wes_period
        try:
            end_time = date2str(sample.accept_time + datetime.timedelta(days), format='%Y-%m-%d')
        except:
            end_time='0000-00-00'
        if not sample:
            return jsonify(status='fail', gene=gene, email_type='check-cnv', msg='this sample does not exists in the CRM')

        user_id = User.query.filter_by(nickname=user).first()
        if not user_id:
            user_id = User.query.filter_by(nickname='bioinfo').first()
        
        gene_list = gene.split(',')
        gene_result = []
        for xx in gene_list:
            xx = xx.strip()
            gene_count = Sample_check_info.query.filter_by(gene_name=xx, sample_id=sample.id).count()
            if gene_count > 0:
                continue
            gene_result.append(xx)
            # check_info = Sample_check_cnv_info(
            #     sample_id=sample.id, 
            #                         gene_name=xx, 
            #                         in_user_id=user_id.id, 
            #                         start_time=datetime.datetime.now()
            #                                 ) 
            check_info = Sample_check_info(
                sample_id=sample.id, 
                                    gene_name=xx, 
                                    user_id=user_id.id,
                                    panel=panel,
                                    check_type='CNV',
                                    start_time=datetime.datetime.now()
                                    
                                            ) 
            db.session.add(check_info)
            # db.session.add(check_info2)
            # print(check_info.json)
            # db.session.add(check_info)
            # print check_info.gene_name
            db.session.commit()
        if gene_result:
            send_email2(configure.cnv_email_list, 
                        '{sample}--{gene}--CNV验证'.format(sample=sample_id, gene=','.join(gene_result)), 
                        'genetron/check_cnv', 
                        sample=sample, 
                        gene=','.join(gene_result),
                       end_time=end_time)
        return jsonify(status='success', gene=','.join(gene_result), email_type='check-cnv', sample=sample_id) 
    
    
api.add_resource(Cnv_Email, '/check-cnv')
        
    