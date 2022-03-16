from arnis_app import app
from flask_user import roles_required
from flask import render_template, request


@app.route('/teacher/dashboard')
@roles_required('teacher')
def teacher_dashboard():
    return render_template('teacher/index.html')


@app.route('/teacher/profile')
@roles_required('teacher')
def teacher_profile():
    pass


@app.route('/teacher/list')
@roles_required('teacher')
def teacher_list():
    pass


@app.route('/teacher/how-to-use')
@roles_required('teacher')
def teacher_instruction():
    pass

