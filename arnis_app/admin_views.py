from arnis_app import app
from flask_user import roles_required
from flask import render_template, request, jsonify, flash, redirect, url_for
from flask_login import current_user
from arnis_app.models import db, UserProfilePic, User, Teacher, Section, Strand, Track, Student, Role, UserRoles, UserProfilePic
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
    section_no = request.form['section_num']
    teacher_id = request.form['teacherID']
    track_id = request.form['trackID']
    strand_id = request.form['strandID']

    sectionQuery = db.session.query(Section).filter_by(section_no=section_no).filter_by(strand_id=strand_id).first()

    # Check input integrity
    if not(section_no == '' or teacher_id == '0' or track_id == '0' or strand_id == '0'):

        # Check if section is already existing
        if not (sectionQuery is None):
            result = 'danger'
            message = 'Section is already registered!'
        else:
            result = 'success'
            message = 'Section has been added!'

            section = Section(
                section_no=section_no,
                teacher_id=teacher_id,
                track_id=track_id,
                strand_id=strand_id
            )

            db.session.add(section)
            db.session.commit()
    else:
        result = 'danger'
        message = 'Invalid inputs!'

    return jsonify({'result': result, 'message': message})


@app.route('/view/teacher', methods=['POST'])
def view_teacher():
    teacher_idq = request.form['teacher_id']

    # Query teacher's info
    teacherInfo = db.session.query(Teacher, User)\
                .outerjoin(User, User.id == Teacher.user_id)\
                .filter(User.id == Teacher.user_id)\
                .filter(Teacher.teacher_id==teacher_idq).first()

    # Query teacher's handled section
    teacherSection = db.session.query(Section, Teacher, Track, Strand)\
                .outerjoin(Teacher, Teacher.teacher_id == Section.teacher_id) \
                .outerjoin(Track, Track.track_id == Section.track_id) \
                .outerjoin(Strand, Strand.strand_id == Section.strand_id) \
                .filter(Teacher.teacher_id == Section.teacher_id) \
                .filter(Track.track_id == Section.track_id) \
                .filter(Strand.strand_id == Section.strand_id) \
                .filter(Teacher.teacher_id==teacher_idq)\
                .with_entities(Section.section_id, Section.section_no, Section.population,
                               Track.name.label('track_name'), Track.nickname.label('track_nickname'),
                               Strand.name.label('strand_name'), Strand.nickname.label('strand_nickname')).all()

    if teacherInfo:
        result = 'single'

        # Transform object to dict
        teacherInfo = vars(teacherInfo[1])
        del teacherInfo['password']
        del teacherInfo['_sa_instance_state']
        del teacherInfo['email_confirmed_at']
        teacherInfo['date_joined'] = str(teacherInfo['date_joined'])

        if teacherSection:
            result = 'both'

            # Transform object to dict
            # Then adding section details to a dict
            sectionList = []

            for i in range(len(teacherSection)):
                section = teacherSection[i]
                section = dict(section)
                if not section['population']:
                    section['population'] = 0

                sectionList.append(section)

            # print(sectionList)
            return jsonify({'result': result, 'teacherInfo': teacherInfo, 'sectionList': sectionList})

        return jsonify({'result': result, 'teacherInfo': teacherInfo})
    else:
        result = 'danger'
        return jsonify({'result': result})


@app.route('/view/student/list', methods=['POST'])
def view_studentList():
    section_idq = request.form['section_id']

    # Query section's list of students
    studentList = db.session.query(Student, Section, User) \
                .outerjoin(Section, Section.section_id == Student.section_id) \
                .outerjoin(User, User.id == Student.user_id) \
                .filter(Section.section_id == Student.section_id) \
                .filter(User.id == Student.user_id) \
                .filter(Section.section_id == section_idq).all()

    # Query section information
    sectionInfo = db.session.query(Section, User, Track, Strand) \
                .outerjoin(Teacher, Teacher.teacher_id == Section.teacher_id) \
                .outerjoin(User, User.id == Teacher.teacher_id) \
                .outerjoin(Track, Track.track_id == Section.track_id) \
                .outerjoin(Strand, Strand.strand_id == Section.strand_id) \
                .filter(Teacher.teacher_id == Section.teacher_id) \
                .filter(User.id == Teacher.teacher_id) \
                .filter(Track.track_id == Section.track_id) \
                .filter(Strand.strand_id == Section.strand_id) \
                .filter(Section.section_id == section_idq).first()

    if sectionInfo:
        result = 'single'
        section = {}
        section.update(vars(sectionInfo[0]))
        section.update(vars(sectionInfo[1]))
        section.update(vars(sectionInfo[2]))
        section['track_name'] = section.pop('name')
        section['track_nickname'] = section.pop('nickname')
        section.update(vars(sectionInfo[3]))
        section['strand_name'] = section.pop('name')
        section['strand_nickname'] = section.pop('nickname')
        del section['password']
        del section['_sa_instance_state']
        del section['email_confirmed_at']
        section['date_joined'] = str(section['date_joined'])
        section['population'] = 0 if not section['population'] else section['population']

        if studentList:
            result = 'both'
            listStudents = []
            for student in studentList:
                dictStudents = {}
                dictStudents.update(vars(student[0]))
                dictStudents.update(vars(student[1]))
                dictStudents.update(vars(student[2]))
                del dictStudents['password']
                del dictStudents['_sa_instance_state']
                del dictStudents['email_confirmed_at']
                dictStudents['date_joined'] = str(dictStudents['date_joined'])

                if dictStudents['middle_name'] == '':
                    dictStudents['middle_name'] = 'None'

                listStudents.append(dictStudents)

            print(listStudents, ' \n', section)
            return jsonify({'result': result, 'listStudents': listStudents, 'sectionInfo': section})
        print(section)
        return jsonify({'result': result, 'sectionInfo': section})
    else:
        result = 'danger'
        return jsonify({'result': result})


@app.route('/section/count/perTeacher', methods=['GET'])
def get_sectionCountPerTeacher():
    # Query number of sections handled by a teacher
    sectionCounts = db.session.query(User.last_name, db.func.count(Section.teacher_id).label('counts'))\
        .select_from(Teacher)\
        .outerjoin(Section, Section.teacher_id == Teacher.teacher_id)\
        .outerjoin(User, User.id == Teacher.user_id)\
        .outerjoin(Track, Track.track_id == Section.track_id)\
        .group_by(User.last_name)\
        .group_by(Section.teacher_id)\
        .order_by('counts')\
        .all()

    sectionCounts = dict(sectionCounts)
    labels = list(sectionCounts.keys())

    return jsonify({'result': 'result!', 'sectionCounts': sectionCounts, 'labels': labels})


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


