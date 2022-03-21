from arnis_app import app
from flask_user import roles_required
from flask import render_template, request
from flask_login import current_user
from arnis_app.models import db, UserProfilePic, User, Teacher, Section, Strand, Track


@app.route('/admin/dashboard')
@roles_required('admin')
def admin_dashboard():
    user_name = current_user.first_name + " " + current_user.last_name
    user_id = current_user.id

    filename = UserProfilePic.query.filter_by(user_id=user_id).first().filename

    teachers = db.session.query(User).join(Teacher, User.id == Teacher.user_id).filter(User.id == Teacher.user_id).all()

    secs = db.session.query(Section, Strand, User.last_name)\
        .join(Strand, Strand.strand_id == Section.strand_id)\
        .join(Teacher, Teacher.teacher_id == Section.teacher_id)\
        .join(User, User.id == Teacher.user_id)

    # print(samp)

    return render_template('admin/index.html', user_name = user_name, filename=filename, teacher=teachers, sec=secs)


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

