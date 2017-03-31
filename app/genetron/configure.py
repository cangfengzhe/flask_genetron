#coding = utf-8

import os

from .. import app_dir


class Configure():
    panel_trans = ['panel509_203', 'panel509_88', 'panel509_51', 'panel203_51']
    panel_clinical = ['panel203', 'panel509', 'panel51', 'panel88', 'WES', 'CT_DNA','panel18', 'panel63']
    UPLOAD_FOLDER = os.path.join(app_dir, 'static', 'upload')
    
