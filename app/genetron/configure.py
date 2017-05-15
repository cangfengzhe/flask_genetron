#coding = utf-8

import os

from .. import app_dir


class Configure():
    panel_trans = ['panel509_203', 'panel509_88', 'panel509_51', 'panel203_51']
    panel_clinical = ['panel203', 'panel509', 'panel51', 'panel88', 'WES', 'CT_DNA','panel18', 'panel63', 'panel68', 'panel39']
    UPLOAD_FOLDER = os.path.join(app_dir, 'static', 'upload')
    
    cnv_email_list = ['yaling.yang@genetronhealth.com', 'qinglin.ding@genetronhealth.com', 'xiaomei.liu@genetronhealth.com',
                'genetron-pm@genetronhealth.com', 'medicalinfo@genetronhealth.com', 'zexiong.niu@genetronhealth.com',
                'hongling.yuan@genetronhealth.com', 'pidong.li@genetronhealth.com', 'can.yang@genetronhealth.com',
               'yali.yan@genetronhealth.com', 'sihui.zhu@genetronhealth.com']
    # cnv_email_list = ['pidong.li@genetronhealth.com', 'bioinfo-auto@genetronhealth.com']
    
    wes_period = 21
    panel_period = 14