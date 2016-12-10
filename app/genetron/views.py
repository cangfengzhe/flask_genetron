#coding=utf-8

from flask import jsonify, request
from flask import render_template
from collections import defaultdict
from models import *
from . import genetron
from flask_login import login_required
import sqlalchemy
import datetime

@genetron.route('/')
def index():
    return render_template('genetron/index.html')

def get_request_data(form):
    '''
    return dict list with data from request.form

    :param form: MultiDict from `request.form`
    :rtype: {id1: {field1:val1, ...}, ...} [fieldn and valn are strings]
    '''

    # request.form comes in multidict [('data[id][field]',value), ...]

    # fill in id field automatically
    data = defaultdict(lambda: {})
    for formkey in form.keys():
        if formkey == 'action':
            data['type'] = form['action']
            # print(data['type'])
            continue
        datapart, idpart, fieldpart = formkey.split('[')
        # if datapart != 'data': raise ParameterError, "invalid input in request: {}".format(formkey)

        idvalue = int(idpart[0:-1])
        fieldname = fieldpart[0:-1]

        data[idvalue][fieldname] = form[formkey]
        data[idvalue]['DT_RowId'] = idvalue
    # return decoded result
    return data


@genetron.route('/patient')
def patient():
    return render_template('genetron/patient.html')

@genetron.route('/patient_info')
def patient_info(id):
    return render_template('genetron/patient_info.html')

@genetron.route('/sample_finish')
def sample_finish():
    return render_template('genetron/sample_finish.html')


@genetron.route('/patient_table')
def patient_table():
    data = Patient_info.query.all()
    return jsonify(
        data=[i.json for i in data]
    )


@genetron.route('/sample')
def sample():
    return render_template('genetron/sample.html')


@genetron.route('/sample_info')
def sample_info():
    id = request.args.get('id')
    smp = Sample_info.query.filter_by(sample_id=id).first_or_404()
    return render_template('genetron/sample_info.html', sample=smp)

@genetron.route('/sample_table')
def sample_table():
    data = Sample_info.query.filter(Sample_info.sample_id.like('%T%') |  Sample_info.panel.like('%ctDNA%'))
    return jsonify(
        data=[i.json for i in data if i.patient]
    )


# 确定报告人
@genetron.route('/report_user', methods=['GET'])
def report_user():
    print(request.args)
    sample = request.args.get('sample')
    report_user = request.args.get('report', 'aa')
    check_user = request.args.get('check')

    return jsonify(
        data= {'aa':report_user, 'bb':check_user}
    )


def proc_bool(var_dict, keys):
    for xx in keys:
        if xx in var_dict:
            if var_dict[xx] == 'true':
                var_dict[xx] = True
            else:
                var_dict[xx] = False
    return var_dict

def proc_date(var_dict, keys):
    for xx in keys:
        if xx in var_dict:
            if not var_dict[xx] == u'':
                var_dict[xx] = datetime.datetime.strptime(var_dict[xx], '%Y-%m-%d').date()
    return var_dict

def proc_now(var_dict, keys):
    for xx in keys:
        if (xx in var_dict) and (var_dict[xx]):
            var_dict[xx + '_time'] = datetime.datetime.now()
    return var_dict


@genetron.route('/sample_response', methods=['GET', 'POST'])
def sample_response():
    form_data = get_request_data(request.form)
    var = [form_data[x] for x in form_data if x != 'type'][0]
    DT_RowId = var['DT_RowId']

    if form_data['type'] == 'remove':
        sample = Sample_info.query.get(int(var['DT_RowId']))
        db.session.delete(sample)
        db.session.commit()
        return jsonify(data=[])
    var = proc_bool(var, ['bioinfo', 'is_finish', 'ask_histology'])
    var = proc_now(var, ['bioinfo', 'is_finish'])
    var = proc_date(var, ['accept_time', 'end_time'])
    if form_data['type'] == 'create':
        var.pop('DT_RowId')

        sample = Sample_info(**var)
        db.session.add(sample)
        db.session.flush()
        db.session.refresh(sample)
        DT_RowId = sample.id
        var['DT_RowId'] = sample.id
        if (('histology' in var) and (not var['histology'] == '')) or (('tissue' in var) and (not var['tissue'] == '')):
            var['get_histology_time'] = datetime.datetime.now()
            var['ask_histology_time'] = True
    elif form_data['type'] == 'edit':
        sample = Sample_info.query.filter_by(id=var['DT_RowId']).first()
        var = proc_now(var, ['bioinfo', 'is_finish', 'ask_histology'])
        if ( ('histology' in var) and (not var['histology'] == '') ) or  (('tissue' in var) and (not var['tissue'] == '')):
            var['get_histology_time'] = datetime.datetime.now()
        sample.from_dict(var)
    print(var)
    db.session.commit()
    dt = Sample_info.query.filter_by(id=DT_RowId).first()
    return jsonify(data=[dt.json])


@genetron.route('/kendo')
def kendo():
    return render_template('genetron/grid.html')



def check_sample(sample_id):
    # 检查sample， 如果sample不在lims中，则添加信息
    sample_id = sample_id.split('-')[0].split('NEW')[0]
    sample_index = Sample_info.query.filter_by(sample_id=sample_id).first()
    print(sample_id)
    if not sample_index:
        print('not link')
        # patient = Patient_info(patient_id=sample_id)
        # db.session.add(patient)
        # db.session.flush()
        # db.session.refresh(patient)
        sample = Sample_info(sample_id=sample_id)
        db.session.add(sample)
        db.session.flush()
        db.session.refresh(sample)
        
        sample_index = sample
        db.session.commit()
    return sample_index

def check_flowcell(flowcell_id):
    flowcell_index = Flowcell_info.query.filter_by(flowcell_id=flowcell_id).first()
    if not flowcell_index:
        flowcell_index = Flowcell_info.query.filter_by(flowcell_id='S00').first()
    return flowcell_index


def link(sample_id, flowcell_id, panel):
    """
    建立sample id， flowcell id联系
    """
    if not sample_id:
        return jsonify(info={'status':'error', 'msg':'sample is null', 'type':'link'})
    sample_index = check_sample(sample_id)
    flowcell_index = Flowcell_info.query.filter_by(flowcell_id=flowcell_id).first()
    if not flowcell_index:
        return jsonify(info={'status':'error', 'msg':'flowcell does not exists', 'type':'link'})
    if not panel:
        return jsonify(info={'status':'error', 'msg':'panel does not exists', 'type':'link'})    
    sample_flowcell = Sample_flowcell.query.filter_by(sample_id=sample_index.id, flowcell_id=flowcell_index.id, panel=panel).first()
    if not sample_flowcell:
        sample_flowcell = Sample_flowcell(sample_id=sample_index.id, flowcell_id=flowcell_index.id, panel=panel)
        db.session.add(sample_flowcell)
        db.session.commit()
        return jsonify(info={'status':'success', 'type':'link'})
    else: 
        return jsonify(info={'status':'exists', 'type':'link'})


def sample_time(sample_id, flowcell_id, panel, item_type, dt,item_note):
    if not sample_id:
        return jsonify(info={'status':'error', 'msg':'sample is null', 'type':item_type})
    #sample_index = Sample_info.query.filter_by(sample_id=sample_id).first()
    sample_index = check_sample(sample_id)
    if not sample_index:
        return jsonify(info={'status':'error', 'msg':'sample is not in LIMS', 'type':item_type})
    if (not flowcell_id) and sample_index.sample_flowcell.order_by(
            sqlalchemy.desc(Sample_flowcell.id)).first(): # 查找该样本最近一次的下机flowcell id
        flowcell_id = sample_index.sample_flowcell.order_by(
            sqlalchemy.desc(Sample_flowcell.id)).first().flowcell.flowcell_id
    if not flowcell_id:
        flowcell_id='S00' # 如果该样本没有对应的flowcell id 那么定义为 S00
    flowcell_index = Flowcell_info.query.filter_by(flowcell_id=flowcell_id).first()
    print(flowcell_id)
    if not flowcell_index:
        flowcell_id='S00'
        flowcell_index = Flowcell_info.query.filter_by(flowcell_id=flowcell_id).first()
        #return jsonify(info={'status':'error', 'msg':'flowcell does not exists', 'type':item_type})
    sample_flowcell = Sample_flowcell.query.filter_by(
                            sample_id=sample_index.id,
                            flowcell_id=flowcell_index.id,
                            panel=panel).first()
    
    # 如果没有sample_flowcell， 可能是 panel 匹配问题，忽略
    if not sample_flowcell:
        link(sample_id, flowcell_id, panel)
        print(sample_index.id, flowcell_index.id)
        sample_flowcell = Sample_flowcell.query.filter_by(
                            sample_id=sample_index.id,
                            flowcell_id=flowcell_index.id
                            ).order_by(sqlalchemy.desc(Sample_flowcell.id)).first()
    if sample_flowcell:
        sample_class = Sample_time_info(sample_flowcell=sample_flowcell.id, item_type=item_type, item_time=dt,item_note=item_note)
        db.session.add(sample_class)
        db.session.commit()
        return jsonify(info={'status':'success', 'type':item_type})
    else:
        return jsonify(info={'status':'error', 'msg': 'the relation between sample and flowcell does not exist', 'type':item_type})





@genetron.route('/api',  methods=['GET', 'POST'])
def api():
    """
    curl "http://127.0.0.1:5000/genetron/api?type=xj_time&time=$(date '+%Y-%m-%d_%H:%M:%S')&flowcell=S05"
    
    """
    api_type = request.args.get('type')
    if not api_type:
        return jsonify(info={'status':'error', 'msg':'type is null', 'type':api_type})
        
    flowcell_id = request.args.get('flowcell')
    
    sample_id = request.args.get('sample')
    dt = request.args.get('time', datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')) # 传入时间使用 %Y-%m-%d_%H:%M:%S
    dt = datetime.datetime.strptime(dt, '%Y-%m-%d_%H%M%S')
    item_note = request.args.get('note')
    panel = request.args.get('panel')
    # http://127.0.0.1:5000/genetron/api?type=sj_time&time=2016-11-26_12:00:00&flowcell=S02
    if api_type == 'sj_time':
        if not flowcell_id:
            return jsonify(info={'status':'error', 'msg':'flowcell is null', 'type':api_type})
        flowcell = Flowcell_info.query.filter_by(flowcell_id=flowcell_id).first()
        if flowcell:
            flowcell.sj_time=dt
            db.session.commit()
        else:
            flowcell=Flowcell_info(flowcell_id=flowcell_id, sj_time=dt)
            db.session.add(flowcell)
            db.session.commit()
        return jsonify(info={'status':'success', 'type':api_type})
    elif api_type == 'xj_time':  
        if not flowcell_id:
            return jsonify(info={'status':'error', 'msg':'flowcell is null', 'type':api_type})
        flowcell = Flowcell_info.query.filter_by(flowcell_id=flowcell_id).first()
        if flowcell:# 如果下机时间只记录一次，不会更新
            if not flowcell.xj_time:
                flowcell.xj_time = dt
                db.session.commit()
        else:
            flowcell = Flowcell_info(flowcell_id=flowcell_id, xj_time=dt)
            db.session.add(flowcell)
            db.session.commit()
        return jsonify(info={'status':'success', 'type':api_type})
    elif api_type == 'cf_time': 
        if not flowcell_id:
            return jsonify(info={'status':'error', 'msg':'flowcell is null', 'type':api_type})
        flowcell = Flowcell_info.query.filter_by(flowcell_id=flowcell_id).first()
        if flowcell:
            flowcell.cf_time = dt # 
            db.session.commit()
        else:
            flowcell = Flowcell_info(flowcell_id=flowcell_id, cf_time=dt)
            db.session.add(flowcell)
            db.session.commit()
        return jsonify(info={'status':'success', 'type':api_type})
    
    elif api_type == 'link':
        return link(sample_id, flowcell_id, panel)
    else:
        return sample_time(sample_id, flowcell_id,panel, api_type, dt,item_note )
        
    

            
    
