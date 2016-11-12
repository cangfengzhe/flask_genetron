import datetime
from flask import jsonify, request
from flask import render_template
from collections import defaultdict
from models import *
from . import genetron
from flask_login import login_required

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




@genetron.route('/', methods=['GET', 'POST'])
@genetron.route('/index', methods=['GET', 'POST'])
@genetron.route('/patient')
def patient():
    return render_template('genetron/patient.html')


@genetron.route('/patient_new')
def patient_new():
    return render_template('genetron/patient_new.html')


@genetron.route('/patient_table')
def patient_table():
    data = Patient_info.query.all()
    return jsonify(
        data=[i.json for i in data]
    )

def sample_table():
    data = Sample_info.query.filter_by('')

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
    var = proc_bool(var, ['bioinfo', 'is_finish', 'ask_histology'])
    var = proc_now(var, ['bioinfo', 'is_finish'])
    var = proc_date(var, ['start_time', 'dead_line'])
    if form_data['type'] == 'remove':
        patient = Patient.query.get(int(var['DT_RowId']))
        db.session.delete(patient)
        db.session.commit()
        return jsonify(data=[])
    if form_data['type'] == 'create':
        var.pop('DT_RowId')
        patient = Patient(**var)
        db.session.add(patient)
        db.session.flush()
        db.session.refresh(patient)
        DT_RowId = patient.id
        var['DT_RowId'] = patient.id
        if (('histology' in var) and (not var['histology'] == '')) or (('tissue' in var) and (not var['tissue'] == '')):
            var['get_histology_time'] = datetime.datetime.now()
            var['ask_histology_time'] = True
    elif form_data['type'] == 'edit':
        patient = Patient.query.filter_by(id=var['DT_RowId']).first()
        var = proc_now(var, ['bioinfo', 'is_finish', 'ask_histology'])
        if ( ('histology' in var) and (not var['histology'] == '') ) or  (('tissue' in var) and (not var['tissue'] == '')):
            var['get_histology_time'] = datetime.datetime.now()
        patient.from_dict(var)
    print(var)
    db.session.commit()
    dt = Sample_info.query.filter_by(id=DT_RowId).first()
    return jsonify(data=[dt.json])
