import os
from flask import Flask
from apps.utils import create_folder

app = Flask(__name__)

app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@106.15.196.160/DeepMoleNet'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

APPS_DIR = os.path.dirname(__file__)

STATIC_DIR = os.path.join(APPS_DIR, 'static')

app.config['UPLOAD_FOLDER'] = "uploads"
app.config['ABS_UPLOAD_FOLDER'] = \
    os.path.join(STATIC_DIR,app.config['UPLOAD_FOLDER'])

create_folder(app.config['ABS_UPLOAD_FOLDER'])
import apps.login