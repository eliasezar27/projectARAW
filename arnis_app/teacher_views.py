from arnis_app import app
from flask_user import roles_required
from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user
from arnis_app.models import db, User, Teacher, Section, Strand, Role, UserRoles, UserProfilePic, Student
from flask_user.translation_utils import gettext as _
from werkzeug.utils import secure_filename
import uuid as uuid
import os
from arnis_app.configs import ConfigClass

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/teacher/dashboard')
@roles_required('teacher')
def teacher_dashboard():
    user_name = current_user.first_name + " " + current_user.last_name
    user_id = current_user.id

    filename = UserProfilePic.query.filter_by(user_id=user_id).first().filename

    user_roles = db.session.query(Role.id, Role.name) \
        .select_from(Role) \
        .outerjoin(UserRoles, UserRoles.role_id == Role.id) \
        .filter(UserRoles.user_id == user_id) \
        .all()

    user_roles = dict(user_roles)
    role_no = len(user_roles)

    student_req = db.session.query(Student, User, Section, Strand, Teacher)\
        .select_from(Student)\
        .outerjoin(User, User.id == Student.user_id)\
        .outerjoin(Section, Section.section_id == Student.request)\
        .outerjoin(Strand, Strand.strand_id == Section.strand_id)\
        .outerjoin(Teacher, Teacher.teacher_id == Section.teacher_id) \
        .filter(Teacher.user_id == user_id) \
        .all()

    student_requests = {}
    if student_req:
        for i in range(len(student_req)):
            student_requests = {}
            student_requests.update(vars(student_req[i][0]))
            student_requests.update(vars(student_req[i][1]))
            student_requests.update(vars(student_req[i][2]))
            student_requests.update(vars(student_req[i][3]))
            student_requests.update(vars(student_req[i][4]))
            del student_requests['password']
            del student_requests['_sa_instance_state']
            del student_requests['email_confirmed_at']
            del student_requests['date_joined']

            student_req[i] = student_requests

    return render_template('teacher/index.html', user_name = user_name,
                           filename=filename, student_requests=student_req, role_no=role_no)


@app.route('/teacher/profile', methods=['GET', 'POST'])
@roles_required('teacher')
def teacher_profile():
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
    role_no = len(user_roles)

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

            return redirect(url_for('teacher_dashboard'))

    return render_template('teacher/profile.html', user_name = user_name, filename=filename,
                           user_info=user_info, user_roles= user_roles, role_no=role_no)


@app.route('/teacher/view-sections')
@roles_required('teacher')
def teacher_viewSections():
    user_name = current_user.first_name + " " + current_user.last_name
    user_id = current_user.id

    filename = UserProfilePic.query.filter_by(user_id=user_id).first().filename

    user_roles = db.session.query(Role.id, Role.name) \
        .select_from(Role) \
        .outerjoin(UserRoles, UserRoles.role_id == Role.id) \
        .filter(UserRoles.user_id == user_id) \
        .all()

    user_roles = dict(user_roles)
    role_no = len(user_roles)

    # Section table join Strand, Teacher, and User Table
    section_list = db.session.query(Section, Strand.name, Strand.track_id) \
        .select_from(Section) \
        .outerjoin(Strand, Strand.strand_id == Section.strand_id) \
        .outerjoin(Teacher, Teacher.teacher_id == Section.teacher_id) \
        .outerjoin(User, User.id == Teacher.user_id) \
        .filter(Teacher.user_id == user_id)\
        .order_by(Section.section_no) \
        .all()

    return render_template('teacher/viewSections.html', user_name = user_name,
                           filename=filename, section_list=section_list, role_no=role_no)