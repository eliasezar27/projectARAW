from arnis_app import app
from flask_user import roles_required
from flask import render_template, request, flash, redirect, url_for, Response
from flask_login import current_user
from arnis_app.models import db, User, Role, UserRoles, UserProfilePic, Student, Section, Teacher, Track, Strand
from flask_user.translation_utils import gettext as _
from werkzeug.utils import secure_filename
import uuid as uuid
import os
from arnis_app.configs import ConfigClass
from arnis_app.camera_source import generate
from arnis_app.camera_source import camera, vs
import threading

t = threading.Thread(target=camera)
t.daemon = True

thread_process = True

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

poses = ['Preparation',
        'Left Temple Strike',
     'Right Temple Strike',
     'Left Arm/Shoulder Strike',
     'Right Arm/Shoulder Strike',
     'Stomach Thrust',
     'Left Chest Thrust',
     'Right Chest Thrust',
     'Right Knee/Leg Strike',
     'Left Knee/Leg Strike',
     'Left Eye Thrust',
     'Right Eye Thrust',
     'Crown Strike',
     'Left Temple Block',
     'Right Temple Block',
     'Left Arm/Shoulder Block',
     'Right Arm/Shoulder Block',
     'Stomach Thrust Block',
     'Left Chest Block',
     'Right Chest Block',
     'Right Knee/Leg Block',
     'Left Knee/Leg Block',
     'Left Eye Block',
     'Right Eye Block',
     'Rising Block']


def allowed_file(filenames):
    return '.' in filenames and filenames.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/student/how-to-use', methods=['GET', 'POST'])
@roles_required('student')
def student_instruction():
    user_name = current_user.first_name + " " + current_user.last_name
    user_id = current_user.id

    filename = UserProfilePic.query.filter_by(user_id=user_id).first().filename

    # check if student belongs to a section
    sectionJoined = db.session.query(Student)\
        .select_from(Student).filter(Student.user_id == user_id).first()

    # Query section list for student options
    sectionLists = db.session.query(Section, Strand, Track, Teacher, User)\
        .outerjoin(Strand, Strand.strand_id == Section.strand_id)\
        .outerjoin(Track, Track.track_id == Strand.track_id)\
        .outerjoin(Teacher, Teacher.teacher_id == Section.teacher_id)\
        .outerjoin(User, User.id == Teacher.user_id).order_by(Section.section_no).all()

    # check if student is reassigned to another section
    reassigned = db.session.query(Student).select_from(Student).filter(Student.user_id == user_id).filter(Student.reassign == 1).first()

    is_reassigned = False
    reassign_msg = ''
    newSection = ()
    if reassigned:
        reassign_msg = reassigned.reason
        is_reassigned = True
        newSection = db.session.query(Section, Student, Strand)\
            .select_from(Section)\
            .outerjoin(Student, Student.section_id == Section.section_id)\
            .outerjoin(Strand, Strand.strand_id == Section.strand_id)\
            .filter(Student.user_id == user_id).first()

    # check if student was removed from a section
    removed_student = db.session.query(Student).select_from(Student).filter(Student.user_id == user_id).filter(Student.removed == 1).first()
    decline_student = db.session.query(Student).select_from(Student).filter(Student.user_id == user_id).filter(Student.request_decision == 0).first()

    remove_msg = ''
    remor_dec = ''
    was_removed = False
    if removed_student or decline_student:
        if removed_student:
            remove_msg = removed_student.reason
            remor_dec = 'You were removed from your previous section, please join another section again.'

        if decline_student:
            remove_msg = decline_student.reason
            remor_dec = 'Your request has been declined by the teacher.'

        was_removed = True

    request_join = db.session.query(Student.request).select_from(Student).filter(Student.user_id == user_id).first()

    requested = True
    wait_section = None
    if None in request_join:
        requested = False
    else:
        wait_section = db.session.query(Section, Student, Strand)\
            .select_from(Section)\
            .outerjoin(Student, Student.request == Section.section_id)\
            .outerjoin(Strand, Strand.strand_id == Section.strand_id)\
            .filter(Student.user_id == user_id).first()

    # print(sectionLists)
    if request.method == "POST":
        section_id = request.form['section_id']

        sectionJoined.request = section_id
        db.session.commit()
        flash(_("You have successfully requested to join a section. Please wait for your to teacher to accept your request."), 'success')
        return redirect(url_for('student_instruction'))

    sectionExist = sectionJoined.section_id is None

    return render_template('student/instruction.html',
                           user_name = user_name, filename=filename, sectionJoined=sectionExist, was_removed=was_removed, remove_msg=remove_msg,
                           sectionLists=sectionLists, is_reassigned=is_reassigned, reassign_msg=reassign_msg, newSection=newSection, requested=requested,
                           wait_section=wait_section, remor_dec=remor_dec)


@app.route('/student/profile', methods=['GET', 'POST'])
@roles_required('student')
def student_profile():
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
            if not (profile_pic.filename == ''):
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

            return redirect(url_for('student_dashboard'))

    return render_template('student/profile.html', user_name = user_name, filename=filename, user_info=user_info, user_roles= user_roles)


@app.route('/student/practice', methods=['GET', 'POST'])
@roles_required('student')
def student_practice():
    global thread_process
    if thread_process:
        t.start()
        thread_process = False

    if vs is not None:
        vs.stop()

    user_name = current_user.first_name + " " + current_user.last_name
    user_id = current_user.id

    filename = UserProfilePic.query.filter_by(user_id=user_id).first().filename

    return render_template('student/practice.html',
                           user_name = user_name, filename=filename)


@app.route('/student/grading', methods=['GET', 'POST'])
@roles_required('student')
def student_grading():
    global thread_process
    if thread_process:
        t.start()
        thread_process = False

    if vs is not None:
        vs.stop()

    user_name = current_user.first_name + " " + current_user.last_name
    user_id = current_user.id

    filename = UserProfilePic.query.filter_by(user_id=user_id).first().filename

    student = db.session.query(Student).filter(Student.user_id==user_id).first()

    if os.path.exists('arnis_app/static/poseResults/' + str(student.student_id)):
        for f in os.listdir('arnis_app/static/poseResults/' + str(student.student_id)):
            os.remove(os.path.join('arnis_app/static/poseResults/' + str(student.student_id), f))

    return render_template('student/grading.html',
                           user_name = user_name, filename=filename, student=student)


@app.route('/student/pose-descriptions', methods=['GET', 'POST'])
@roles_required('student')
def student_description():

    user_name = current_user.first_name + " " + current_user.last_name
    user_id = current_user.id

    filename = UserProfilePic.query.filter_by(user_id=user_id).first().filename

    pose_imgs = os.listdir('arnis_app/static/images/poses')

    pose_descs = []
    with open('arnis_app/static/images/pose_descriptions.txt') as f:
        for line in f:
            pose_descs.append(line.replace('\n', ''))

    hash = []
    with open('arnis_app/static/images/youtube_links.txt') as h:
        for ln in h:
            hash.append(ln.replace('\n', ''))

    return render_template('student/description.html',
                           user_name=user_name, filename=filename, poses=poses, pose_imgs=pose_imgs, pose_descs=pose_descs, hash=hash)


@app.route('/student/results', methods=['GET', 'POST'])
@roles_required('student')
def student_results():
    user_name = current_user.first_name + " " + current_user.last_name
    user_id = current_user.id

    filename = UserProfilePic.query.filter_by(user_id=user_id).first().filename

    student = db.session.query(Student).filter(Student.user_id == user_id).first()

    user_images = []
    if os.path.exists('arnis_app/static/poseResults/' + str(student.student_id)):
        user_images = os.listdir('arnis_app/static/poseResults/' + str(student.student_id))

    if len(user_images) > 0:
        for i in range(len(user_images)):
            user_images[i] = 'poseResults/' + str(student.student_id) + '/' + user_images[i]

    return render_template('student/results.html',
                           user_name=user_name, filename=filename, student=student, user_images=user_images)


@app.route('/video_feed')
@roles_required('student')
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")