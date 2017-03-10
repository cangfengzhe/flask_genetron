#coding=utf-8

from flask import jsonify, request, flash
from flask import render_template,redirect, url_for, current_app
from collections import defaultdict

from flask_login import login_required
import sqlalchemy
import datetime

from ..models import User
from forms import *
from models import *
from . import genetron
from  configure import Configure as configure


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


@genetron.route('/sample2')
def sample2():
    return render_template('genetron/sample.html')


@genetron.route('/sample_info')
def sample_info():
    id = request.args.get('id')
    smp = Sample_info.query.filter_by(sample_id=id).first_or_404()
    return render_template('genetron/sample_info.html', sample=smp)

@genetron.route('/sample_table')
def sample_table():
    # data = Sample_info.query.filter(Sample_info.sample_id.like('%T%') |  Sample_info.panel.like('%ctDNA%') | Sample_info.panel.like('%63%'))
    data = Sample_info.query.filter_by(is_show=1)
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



def check_sample(sample_id):
    # 检查sample， 如果sample不在lims中，则添加信息
    sample_id = sample_id.split('-')[0].split('NEW')[0]
    sample_index = Sample_info.query.filter_by(sample_id=sample_id).first()
    if not sample_index:
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

    
def set_sample_flowcell_time(sample_flowcell, item, value=None, user='bioinfo'):
    sf = Sample_flowcell_info.query.filter_by(sample_flowcell=sample_flowcell.id).first()
    if  sf:
        if item == 'bioinfo_report_time':
            sf.bioinfo_finish = True
            if User.query.filter_by(nickname=user).first():
                user_id = User.query.filter_by(nickname=user).first().id
            else:
                user_id = User.query.filter_by(nickname='bioinfo').first().id
            sf.user_id = user_id
        setattr(sf, item, value) 
    else:
        sf = Sample_flowcell_info(sample_flowcell=sample_flowcell.id)
        setattr(sf, item, value)
    db.session.add(sf)
    db.session.commit()         


def sample_time(sample_id, flowcell_id, panel, item_type, dt, item_note, user):
    
    if not sample_id:
        return jsonify(info={'status':'error', 'msg':'sample is null', 'type':item_type})
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
        sample_class = Sample_time_info(sample_flowcell=sample_flowcell.id, item_type=item_type, item_time=dt, item_note=item_note)
        db.session.add(sample_class)
        db.session.commit()
        # sample_flowcell_info = Sample_flowcell_info(sample_flowcell=sample_flowcell, )
        
        # 写入 sample_flowcell_info 表
        if item_type in ['class', 'submit', 'bioinfo_finish', 'bioinfo_report']:
            print(item_type)
            item_type_time = item_type + '_time'
            set_sample_flowcell_time(sample_flowcell, item_type_time, dt, user)
            
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
    import datetime
    dt = request.args.get('time', datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')) # 传入时间使用 %Y-%m-%d_%H:%M:%S
    dt = datetime.datetime.strptime(dt, '%Y-%m-%d_%H:%M:%S')
    item_note = request.args.get('note')
    panel = request.args.get('panel')
    user = request.args.get('user', 'bioinfo')
    if panel:
        if panel == 'exome' or panel == 'WES+88' or panel == 'WES+panel88':
            panel = 'WES'
        if ('_' in panel) and ('CT' not in panel) and ('germline' not in panel):  # 转平台panel处理
            panel = 'panel' + panel.split('_')[1]
        if ('CT' in panel) or ('ct' in panel):
            print('panel',panel)
            panel = 'CT_DNA'
    # http://127.0.0.1:5000/genetron/api?type=sj_time&time=2016-11-26_12:00:00&flowcell=S02
    if api_type == 'sj_time':
        if not flowcell_id:
            return jsonify(info={'status':'error', 'msg':'flowcell is null', 'type':api_type})
        flowcell = Flowcell_info.query.filter_by(flowcell_id=flowcell_id).first()
        if flowcell:
            flowcell.sj_time = dt
            db.session.commit()
        else:
            flowcell = Flowcell_info(flowcell_id=flowcell_id, sj_time=dt)
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
        return sample_time(sample_id, flowcell_id, panel, api_type, dt,item_note, user)

    
@genetron.route('/check_info',  methods=['GET', 'POST'])    
def check_info():
    '''添加验证（CNV、MSI）信息
    '''
    flowcell = request.values.get('flowcell', '')
    panel = request.values.get('panel', '')
    sample_id = request.values.get('sample','')
    check_type = request.values.get('check_type', '')
    gene = request.values.get('gene', '')
    start_time_str = request.values.get('start_time')
    start_time = datetime.datetime.strptime(start_time_str, '%Y-%m-%d %HH:%MM').datetime() if start_time_str else None
    end_time_str = request.values.get('end_time')
    end_time = datetime.datetime.strptime(end_time_str, '%Y-%m-%d %HH:$MM').datetime() if end_time_str else None
    result = request.values.get('result', '')
    note = request.values.get('note', '')
    sample_index = Sample_info.query.filter_by(sample_id=sample_id).first()
    
    return jsonify(info={'status':'success', 'type':'check'})

@genetron.route('/unfinish',  methods=['GET', 'POST'])
@genetron.route('/todo',  methods=['GET', 'POST'])
def unfinish():          
    return render_template('genetron/sample_unfinish.html')


@genetron.route('/mut_stat',  methods=['GET', 'POST'])
def mut_stat():          
    return render_template('genetron/mut_stat.html')


@genetron.route('/help',  methods=['GET', 'POST'])
def help():
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
            current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
            
    # doc_type_id=1 means Help
    pagination = Document.query.filter_by(doc_type_id=1).order_by(Document.create_time.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    items = pagination.items
    return render_template('genetron/help.html', items=items, pagination=pagination)


@genetron.route('/update',  methods=['GET', 'POST'])
def update():
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
            current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
            
    # doc_type_id=1 means Help
    pagination = Document.query.filter_by(doc_type_id=2).order_by(Document.create_time.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    items = pagination.items
    return render_template('genetron/update.html', items=items, pagination=pagination)


@genetron.route('/barcode',  methods=['GET'])
def barcode():          
    return render_template('genetron/barcode.html')


@genetron.route('/submit/', methods=['GET', 'POST'])
@login_required
def submit():
    # D = Post.query.get_or_404(id)
    form = DocumentForm()
    if form.validate_on_submit():
        document = Document(title=form.title.data,
                     body=form.body.data,
                     doc_type_id=form.doc_type_id.data,
                     user_id=current_user.id,
                     create_time = datetime.datetime.now()
                     )
        db.session.add(document)
        db.session.commit()
        flash('Your comment has been published.')
        return redirect(url_for('.submit'))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
            current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = Document.query.order_by(Document.create_time.asc()).paginate(
        page, per_page=5,  # current_app.config['FLASKY_COMMENTS_PER_PAGE']
        error_out=False)
    items = pagination.items
    return render_template('genetron/submit.html', form=form, items=items, pagination=pagination)
  

@genetron.route('/document/<int:id>', methods=['GET', 'POST'])
def document(id):
    doc = Document.query.get_or_404(id)
    
    return render_template('genetron/document.html', doc=doc)


@genetron.route('/pgm-submit/', methods=['GET', 'POST'])
def pgm_submit():
    form = PGMForm()
    #pgm = Flowcell_info.query.filter(Flowcell_info.flowcell_id.like('PGM%'))
    
    if form.validate_on_submit():        
        flowcell = Flowcell_info(flowcell_id=form.pgm_id.data, xj_time=form.xj_time.data)
        db.session.add(flowcell)
        db.session.commit()
        flowcell_id = form.pgm_id.data
        sample_list = set([xx.split('-')[0] for xx in form.sample_list.data.strip().split('\n')])
        for sample_id in sample_list:
            link(sample_id, flowcell_id, 'panel51')
            try:
                sample_time(sample_id, flowcell_id, 'panel51', 'class', form.xj_time.data, '')
            except:
                pass
        db.session.commit()
        flash('The PGM Info has been created.')
        return redirect(url_for('.pgm_submit'))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
            current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = Flowcell_info.query.filter(Flowcell_info.flowcell_id.like('%PGM')).order_by(Flowcell_info.xj_time.asc()).paginate(
        page, per_page=5,  # current_app.config['FLASKY_COMMENTS_PER_PAGE']
        error_out=False)
    items = pagination.items
    
    return render_template('genetron/PGM.html', form=form, items=items, pagination=pagination)


@genetron.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_doc(id):
    doc = Document.query.get_or_404(id)
    if doc.user_id != current_user.id:
        flash('You cannt edit others document')
        return redirect(url_for('.document', id=id))
    form = EditDocumentForm()
    if form.validate_on_submit():
        print form
        doc.title = form.title.data
        doc.body = form.body.data
        doc.doc_type_id = form.doc_type_id.data
        doc.change_time = datetime.datetime.now()
        # db.session.add(doc)
        db.session.commit()
        flash('Your document has been update.')
        return redirect(url_for('.document', id=id))
    else:
        form.title.data = doc.title
        form.body.data = doc.body 
        form.doc_type_id.data = doc.doc_type
        return render_template('genetron/edit_document.html', doc=doc, form=form)

@genetron.route('/sample/', methods=['GET', 'POST'])
def sample():
    return render_template('genetron/sample2.html')