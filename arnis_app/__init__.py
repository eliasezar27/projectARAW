from flask import Flask
from .configs import ConfigClass

app = Flask(__name__)
app.config.from_object(__name__ + '.ConfigClass')

from arnis_app import public_views
from arnis_app import admin_views
from arnis_app import student_views
from arnis_app import teacher_views
from arnis_app import async_request
from arnis_app import camera_source




