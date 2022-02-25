from flask import Flask

app = Flask(__name__)

from arnis_app import public_views
from arnis_app import student_views
from arnis_app import teacher_views




