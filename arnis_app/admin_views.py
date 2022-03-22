from arnis_app import app
from flask_user import roles_required
from flask import render_template, request, jsonify
from flask_login import current_user
from arnis_app.models import db, UserProfilePic, User, Teacher, Section, Strand, Track


@app.route('/admin/dashboard')
@roles_required('admin')
def admin_dashboard():
    user_name = current_user.first_name + " " + current_user.last_name
    user_id = current_user.id

    filename = UserProfilePic.query.filter_by(user_id=user_id).first().filename

    teachers = db.session.query(Teacher, User)\
        .outerjoin(User, User.id == Teacher.user_id).filter(User.id == Teacher.user_id).order_by(User.last_name).all()

    # Section table join Strand, Teacher, and User Table
    secs = db.session.query(Section, Strand.nickname, User)\
        .outerjoin(Strand, Strand.strand_id == Section.strand_id)\
        .outerjoin(Teacher, Teacher.teacher_id == Section.teacher_id)\
        .outerjoin(User, User.id == Teacher.user_id).all()

    tracks = Track.query.all()

    strands = Strand.query.all()

    return render_template('admin/index.html',
                           user_name = user_name, filename=filename, teacher=teachers, sec=secs,
                           tracks=tracks, strands=strands)


@app.route('/add_section', methods=['POST'])
def add_section():

    section = Section(
        section_no=request.form['section_num'],
        teacher_id=request.form['teacherID'],
        track_id=request.form['trackID'],
        strand_id=request.form['strandID']
    )

    db.session.add(section)
    db.session.commit()

    return jsonify({'result': 'success'})


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

