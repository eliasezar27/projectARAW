from arnis_app import app
from flask import render_template, request


from arnis_app import app
from flask import render_template, request


@app.route('/teacher-dashboard')
def teacher_dashboard():
    return '<h1>Welcome to teacher dashboard</h1>'


@app.route('/teacher-profile')
def teacher_profile():
    pass


@app.route('/teacher-list')
def teacher_list():
    pass


@app.route('/teacher/how-to-use')
def teacher_instruction():
    pass

