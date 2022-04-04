from arnis_app import app
from flask_user import roles_required
from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user
from arnis_app.models import db, User, Teacher, Section, Strand, Track, Role, UserRoles, UserProfilePic
from flask_user.translation_utils import gettext as _
from werkzeug.utils import secure_filename
import uuid as uuid
import os
from arnis_app.configs import ConfigClass

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/admin/dashboard')
@roles_required('admin')
def admin_dashboard():
    user_name = current_user.first_name + " " + current_user.last_name
    user_id = current_user.id

    filename = UserProfilePic.query.filter_by(user_id=user_id).first().filename

    # Section table join Strand, Teacher, and User Table
    secs = db.session.query(Section, Strand.nickname, User)\
        .outerjoin(Strand, Strand.strand_id == Section.strand_id)\
        .outerjoin(Teacher, Teacher.teacher_id == Section.teacher_id)\
        .outerjoin(User, User.id == Teacher.user_id).all()

    tracks = Track.query.all()

    strands = Strand.query.all()

    return render_template('admin/index.html',
                           user_name = user_name, filename=filename,sec=secs,
                           tracks=tracks, strands=strands)


@app.route('/admin/profile', methods=['GET', 'POST'])
@roles_required('admin')
def admin_profile():
    user_name = current_user.first_name + " " + current_user.last_name
    user_id = current_user.id
    user_email = current_user.email
    user_mobile = current_user.mobile
    user_first_name = current_user.first_name
    user_last_name = current_user.last_name

    user_roles = db.session.query(Role.id, Role.name) \
        .select_from(Role) \
        .outerjoin(UserRoles, UserRoles.role_id == Role.id) \
        .filter(UserRoles.user_id == user_id) \
        .all()

    user_roles = dict(user_roles)

    user_info = {'email': user_email, 'mobile': user_mobile, 'firstname': user_first_name, 'lastname': user_last_name}

    filename = UserProfilePic.query.filter_by(user_id=user_id).first().filename

    if request.method == "POST":
        if 'profileImg' in request.files:
            profile_pic = request.files['profileImg']
            if not(profile_pic.filename == ''):
                pic_filename = secure_filename(profile_pic.filename)
                if allowed_file(profile_pic.filename):
                    pic_filename = pic_filename.replace(" ", "_")
                    pic_filename = str(uuid.uuid1()) + "_" + pic_filename
                    profile_pic.save(os.path.join(ConfigClass.UPLOAD_FOLDER, pic_filename))

                    profile_table = UserProfilePic.query.filter_by(user_id=user_id).first()
                    profile_table.filename = os.path.join("profile_pic/", pic_filename)

                    flash(_("Image successfully uploaded."), 'success')

                else:
                    flash(_("'%(file)' Unsupported file type.", file=profile_pic.filename), 'error')

            new_email = request.form['email']
            new_mobile = request.form['pnum']
            new_given = request.form['first_name']
            new_last = request.form['last_name']

            User.query.filter_by(id=user_id).first().email = new_email
            User.query.filter_by(id=user_id).first().mobile = new_mobile
            User.query.filter_by(id=user_id).first().last_name = new_last
            User.query.filter_by(id=user_id).first().first_name = new_given

            db.session.commit()

            flash(_("Profile successfully updated."), 'success')

            return redirect(url_for('admin_dashboard'))

    return render_template('admin/profile.html', user_name = user_name, filename=filename, user_info=user_info, user_roles= user_roles)


@app.route('/admin/view-teachers')
@roles_required('admin')
def admin_viewTeachers():
    user_name = current_user.first_name + " " + current_user.last_name
    user_id = current_user.id

    filename = UserProfilePic.query.filter_by(user_id=user_id).first().filename

    teachers = db.session.query(Teacher, User)\
        .outerjoin(User, User.id == Teacher.user_id).filter(User.id == Teacher.user_id).order_by(User.last_name).all()

    return render_template('admin/viewTeachers.html',
                           user_name = user_name, filename=filename, teacher=teachers)


@app.route('/admin/view-sections')
@roles_required('admin')
def admin_viewSections():
    user_name = current_user.first_name + " " + current_user.last_name
    user_id = current_user.id

    filename = UserProfilePic.query.filter_by(user_id=user_id).first().filename

    teachers = db.session.query(Teacher, User) \
        .outerjoin(User, User.id == Teacher.user_id).filter(User.id == Teacher.user_id).order_by(User.last_name).all()

    tracks = db.session.query(Track).all()
    strands = db.session.query(Strand).all()

    return render_template('admin/viewSections.html',
                           user_name = user_name, filename=filename, teachers=teachers, tracks=tracks, strands=strands)


@app.route('/admin/view-students')
@roles_required('admin')
def admin_viewStudents():
    user_name = current_user.first_name + " " + current_user.last_name
    user_id = current_user.id

    filename = UserProfilePic.query.filter_by(user_id=user_id).first().filename

    return render_template('admin/viewStudents.html',
                           user_name = user_name, filename=filename)


@app.route('/admin/tracks-strands')
@roles_required('admin')
def admin_editTracks():
    user_name = current_user.first_name + " " + current_user.last_name
    user_id = current_user.id

    filename = UserProfilePic.query.filter_by(user_id=user_id).first().filename

    return render_template('admin/editTracks.html',
                           user_name = user_name, filename=filename)