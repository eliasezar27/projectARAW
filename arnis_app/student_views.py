from arnis_app import app
from flask_user import roles_required
from flask import render_template, request


@app.route('/student/dashboard')
@roles_required('student')
def student_dashboard():
    return render_template('student/index.html')


@app.route('/student/profile')
@roles_required('student')
def student_profile():
    pass


@app.route('/student/results')
@roles_required('student')
def student_results():
    pass


@app.route('/student/process')
@roles_required('student')
def student_process():
    pass


@app.route('/student/pose-desc')
@roles_required('student')
def poseDesc():
    pass


@app.route('/student/how-to-use')
@roles_required('student')
def student_instruction():
    pass

