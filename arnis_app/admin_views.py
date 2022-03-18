from arnis_app import app
from flask_user import roles_required
from flask import render_template, request


@app.route('/admin/dashboard')
@roles_required('admin')
def admin_dashboard():
    return render_template('admin/index.html')


@app.route('/admin/profile')
@roles_required('admin')
def admin_profile():
    pass


@app.route('/admin/results')
@roles_required('admin')
def admin_results():
    pass


@app.route('/admin/process')
@roles_required('admin')
def admin_process():
    pass


@app.route('/admin/how-to-use')
@roles_required('admin')
def admin_instruction():
    pass

