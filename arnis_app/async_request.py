from arnis_app.models import db, User, Teacher, Section, Strand, Track, Student, Activity, UserRoles
from flask import request, jsonify, flash
from arnis_app import app
from flask_login import current_user
from flask_user.translation_utils import gettext as _
from arnis_app.camera_source import ave_grade
import json
import datetime
from statistics import mean


@app.route('/add_section', methods=['POST'])
def add_section():
    section_no = request.form['section_num']
    teacher_id = request.form['teacherID']
    track_id = request.form['trackID']
    strand_id = request.form['strandID']

    sectionQuery = db.session.query(Section).filter_by(section_no=section_no).filter_by(strand_id=strand_id).first()

    # Check input integrity
    if not(section_no == '' or teacher_id == '0' or track_id == '' or strand_id == ''):

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
                strand_id=strand_id
            )

            db.session.add(section)
            db.session.commit()
    else:
        result = 'danger'
        message = 'Invalid inputs!'

    return jsonify({'result': result, 'message': message})


# Teacher Info Viewer
@app.route('/view/teacher', methods=['GET'])
def view_teacher():
    teacher_idq = request.args.get('teacher_id')

    # Query teacher's info
    teacherInfo = db.session.query(Teacher, User)\
                .outerjoin(User, User.id == Teacher.user_id)\
                .filter(User.id == Teacher.user_id)\
                .filter(Teacher.teacher_id==teacher_idq).first()

    userRole = db.session.query(UserRoles) \
        .select_from(UserRoles)\
        .outerjoin(Teacher, Teacher.user_id == UserRoles.user_id) \
        .filter(UserRoles.user_id == Teacher.user_id)\
        .filter(Teacher.teacher_id == teacher_idq).all()

    is_admin = 0
    if userRole:
        for i in range(len(userRole)):
            userRole[i] = userRole[i].role_id

        if 1 in userRole:
            is_admin = 1

    if teacherInfo:
        result = 'success'

        # Transform object to dict
        teach = vars(teacherInfo[0])
        teacherInfo = vars(teacherInfo[1])
        teacherInfo.update(teach)
        del teacherInfo['password']
        del teacherInfo['_sa_instance_state']
        del teacherInfo['email_confirmed_at']
        teacherInfo['date_joined'] = str(teacherInfo['date_joined'])

        return jsonify({'result': result, 'teacherInfo': teacherInfo, 'is_admin': is_admin})
    else:
        result = 'danger'
        return jsonify({'result': result})


# Student list viewer
@app.route('/view/student/list', methods=['GET'])
def view_studentList():
    section_idq = request.args.get('section_id')

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
                .outerjoin(Strand, Strand.strand_id == Section.strand_id) \
                .outerjoin(Track, Track.track_id == Strand.track_id) \
                .filter(Teacher.teacher_id == Section.teacher_id) \
                .filter(User.id == Teacher.teacher_id) \
                .filter(Strand.strand_id == Section.strand_id) \
                .filter(Track.track_id == Strand.track_id) \
                .filter(Section.section_id == section_idq).first()

    section = {}
    if sectionInfo:
        result = 'success'
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

        listStudents = []
        if studentList:
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

        return jsonify({'result': result, 'listStudents': listStudents, 'sectionInfo': section})
        # print(section)
        # return jsonify({'result': result, 'sectionInfo': section})
    else:
        result = 'danger'
        return jsonify({'result': result})


# Admin column chart
@app.route('/section/count/perTeacher', methods=['GET'])
def get_sectionCountPerTeacher():
    # Query number of sections handled by a teacher
    sectionCounts = db.session.query(User.last_name, db.func.count(Section.teacher_id).label('counts'))\
        .select_from(Teacher)\
        .outerjoin(Section, Section.teacher_id == Teacher.teacher_id)\
        .outerjoin(User, User.id == Teacher.user_id)\
        .outerjoin(Strand, Strand.strand_id == Section.strand_id)\
        .group_by(User.last_name)\
        .group_by(Section.teacher_id)\
        .order_by(db.desc('counts'))\
        .all()

    sectionCounts = dict(sectionCounts)
    labels = list(sectionCounts.keys())

    return jsonify({'result': 'result!', 'sectionCounts': sectionCounts, 'labels': labels})


# Teacher column chart
@app.route('/section/count/perTrack', methods=['GET'])
def get_sectionCountPerTrack():

    user_id = current_user.id

    # Query number of sections per Track handled by a teacher
    sectionCounts = db.session.query(Track.nickname, db.func.count(Strand.track_id).label('counts')) \
        .select_from(Section) \
        .outerjoin(Strand, Strand.strand_id == Section.strand_id)\
        .outerjoin(Track, Track.track_id == Strand.track_id) \
        .outerjoin(Teacher, Teacher.teacher_id == Section.teacher_id) \
        .filter(Teacher.user_id == user_id)\
        .group_by(Track.nickname) \
        .order_by(db.desc('counts'))\
        .all()

    sectionCounts = dict(sectionCounts)
    track_names = list(dict(db.session.query(Track.track_id, Track.nickname).select_from(Track).all()).values())
    labels = list(sectionCounts.keys())

    for i in track_names:
        if not(i in labels):
            labels.append(i)

    return jsonify({'result': 'result!', 'sectionCounts': sectionCounts, 'labels': labels})


# Status changer in admin module
@app.route('/change/user/status', methods=['POST'])
def change_UserStatus():
    user_id = request.form['user_id']
    userStatus = request.form['userStatus']

    user = db.session.query(User).filter(User.id == user_id).first()
    user.active = int(userStatus)

    db.session.commit()

    return jsonify({'result': 'success', 'status': userStatus})


# Status changer in admin module
@app.route('/assign/admin', methods=['POST'])
def assign_admin():
    user_id = int(request.form['user_id'])
    adminStatus = int(request.form['adminStatus'])

    userRoles = db.session.query(UserRoles).filter(UserRoles.user_id == user_id).order_by(UserRoles.role_id).all()

    for i in range(len(userRoles)):
        userRoles[i] = userRoles[i].role_id

    if adminStatus == 1:  # assign teacher as admin

        if not(1 in userRoles or None in userRoles):
            add_admin = UserRoles(
                user_id=user_id,
                role_id=adminStatus
            )
            db.session.add(add_admin)
        else:
            set_admin = db.session.query(UserRoles).filter(UserRoles.user_id == user_id).filter(UserRoles.role_id == None).first()
            set_admin.role_id = adminStatus

    else:  # unassigned teacher as admin
        unset_admin = db.session.query(UserRoles).filter(UserRoles.user_id == user_id).filter(UserRoles.role_id == 1).first()
        unset_admin.role_id = None

    db.session.commit()

    return jsonify({'result': 'success', 'status': adminStatus})


@app.route('/view/section/list', methods=['GET'])
def view_sectionList():
    teacher_idq = request.args.get('teacher_id')

    # Query teacher's sections
    sectionList = db.session.query(Section.section_id,
                                   Section.population,
                                   Section.section_no,
                                   Track.name.label('track_name'),
                                   Track.nickname.label('track_nickname'),
                                   Strand.name.label('strand_name'),
                                   Strand.nickname.label('strand_nickname'))\
        .select_from(Section) \
        .outerjoin(Strand, Strand.strand_id == Section.strand_id) \
        .outerjoin(Track, Track.track_id == Strand.track_id) \
        .outerjoin(Teacher, Teacher.teacher_id == Section.teacher_id) \
        .outerjoin(User, User.id == Teacher.user_id) \
        .filter(Teacher.teacher_id == teacher_idq).all()

    teacherInfo = db.session.query(Teacher, User) \
        .outerjoin(User, User.id == Teacher.user_id) \
        .filter(User.id == Teacher.user_id) \
        .filter(Teacher.teacher_id == teacher_idq).first()

    if teacherInfo:
        result = 'success'

        # Transform object to dict
        teach = vars(teacherInfo[0])
        teacherInfo = vars(teacherInfo[1])
        teacherInfo.update(teach)
        del teacherInfo['password']
        del teacherInfo['_sa_instance_state']
        del teacherInfo['email_confirmed_at']
        del teacherInfo['date_joined']

        if sectionList:

            for i in range(len(sectionList)):
                sectionList[i] = dict(sectionList[i])

        return jsonify({'result': result, 'sectionList': sectionList, 'teacherInfo': teacherInfo})
    else:
        result = 'danger'
        return jsonify({'result': result})


# Teacher Info Viewer
@app.route('/view/student/info', methods=['GET'])
def view_studentInfo():
    student_idq = request.args.get('student_id')

    # Query student's info
    studentInfo = db.session.query(Student, User)\
                .select_from(Student)\
                .outerjoin(User, User.id == Student.user_id)\
                .filter(Student.student_id==student_idq).first()

    if studentInfo:
        result = 'success'

        # Transform object to dict
        teach = vars(studentInfo[0])
        studentInfo = vars(studentInfo[1])
        studentInfo.update(teach)
        del studentInfo['password']
        del studentInfo['_sa_instance_state']
        del studentInfo['email_confirmed_at']
        studentInfo['date_joined'] = str(studentInfo['date_joined'])

        print(studentInfo)
        if studentInfo['section_id']:
            # Query student's section info
            sectionInfo = db.session.query(Section, Strand, Track, Teacher, User) \
                .select_from(Section) \
                .outerjoin(Strand, Strand.strand_id == Section.strand_id) \
                .outerjoin(Track, Track.track_id == Strand.track_id) \
                .outerjoin(Teacher, Teacher.teacher_id == Section.teacher_id) \
                .outerjoin(User, User.id == Teacher.user_id) \
                .filter(Section.section_id == studentInfo['section_id']).first()

            studentSectionInfo = {}
            if sectionInfo:
                result = 'success'

                # Transform object to dict
                studentSectionInfo.update(vars(sectionInfo[0]))
                studentSectionInfo.update(vars(sectionInfo[1]))
                studentSectionInfo['strand_name'] = studentSectionInfo.pop('name')
                studentSectionInfo['strand_nickname'] = studentSectionInfo.pop('nickname')
                studentSectionInfo.update(vars(sectionInfo[2]))
                studentSectionInfo['track_name'] = studentSectionInfo.pop('name')
                studentSectionInfo['track_nickname'] = studentSectionInfo.pop('nickname')
                studentSectionInfo.update(vars(sectionInfo[3]))
                studentSectionInfo.update(vars(sectionInfo[4]))
                del studentSectionInfo['password']
                del studentSectionInfo['_sa_instance_state']
                del studentSectionInfo['email_confirmed_at']
                del studentSectionInfo['date_joined']

                print(studentSectionInfo)

                return jsonify({'result': result, 'studentInfo': studentInfo, 'studentSectionInfo': studentSectionInfo})

        return jsonify({'result': result, 'studentInfo': studentInfo})
    else:
        result = 'danger'
        return jsonify({'result': result})


@app.route('/view/strand/list', methods=['GET'])
def view_strandList():
    track_idq = request.args.get('track_id')
    strand_list = db.session.query(Strand).filter(Strand.track_id == track_idq).all()
    for i in range(len(strand_list)):
        strand_list[i] = vars(strand_list[i])
        strand_list[i].pop('_sa_instance_state')

    return jsonify({'result': 'success', 'strand_list': strand_list})


@app.route('/edit_track', methods=['POST'])
def edit_track():
    track_id = request.form['track_id']
    track_name = request.form['track_name']
    track_nickname = request.form['track_nickname']

    trackQuery = db.session.query(Track).filter_by(track_id=track_id).first()
    check_trackName = db.session.query(Track).filter_by(name=track_name).first()
    check_trackNickname = db.session.query(Track).filter_by(nickname=track_nickname).first()

    message = ''
    # Check if track name is already existing
    if check_trackName or check_trackNickname:
        result = 'danger'
        if check_trackName:
            message = 'Track name already exists!'
        if check_trackNickname:
            message = 'Track code already exists!'

    else:

        trackQuery.name = track_name
        trackQuery.nickname = track_nickname

        db.session.commit()

        result = 'success'
        message = 'Track has been edited!'

    return jsonify({'result': result, 'message': message})


@app.route('/add_strand', methods=['POST'])
def add_strand():
    track_id = request.form['track_id']
    strand_name = request.form['strand_name']
    strand_nickname = request.form['strand_nickname']

    strandNameQuery = db.session.query(Strand).filter_by(name=strand_name).first()
    strandNicknameQuery = db.session.query(Strand).filter_by(nickname=strand_nickname).first()

    print(strandNameQuery)
    print(strandNicknameQuery)

    message = ''
    # Check input integrity
    if not(strand_name == '' or strand_nickname == '' or track_id == ''):

        # Check if section is already existing
        if not (strandNameQuery is None and strandNicknameQuery is None):
            result = 'danger'

            if not (strandNameQuery is None):
                message = 'Strand Name is already existing!'

            if not (strandNicknameQuery is None):
                message = 'Strand Code is already existing!'
        else:
            result = 'success'
            message = 'new strand has been added!'

            strand = Strand(
                name=strand_name,
                nickname=strand_nickname,
                track_id=int(track_id)
            )

            db.session.add(strand)
            db.session.commit()
    else:
        result = 'danger'
        message = 'Invalid inputs!'

    return jsonify({'result': result, 'message': message})


@app.route('/get/student/info', methods=['GET'])
def get_studentInfo():
    student_idq = request.args.get('student_id')

    student = db.session.query(Student, User)\
        .select_from(Student)\
        .outerjoin(User, User.id == Student.user_id)\
        .filter(Student.student_id == student_idq).first()

    student_info = {}

    student_info.update(vars(student[0]))
    student_info.update(vars(student[1]))
    student_info.pop('_sa_instance_state')
    student_info.pop('password')

    return jsonify({'result': 'success', 'student_info': student_info})


@app.route('/transfer/section', methods=['POST'])
def transfer_section():
    student_id = int(request.form['student_id'])
    section_id = int(request.form['section_id'])
    reason = request.form['reasonAction']
    transfer = db.session.query(Student).filter(Student.student_id == student_id).first()

    # new section
    section_transfer = db.session.query(Section).filter(Section.section_id == section_id).first()

    # old section
    section_id_remove = transfer.section_id
    section_remove = db.session.query(Section).filter(Section.section_id == section_id_remove).first()

    if transfer is None:
        result = 'danger'
        message = 'Student not recognized!'
    else:
        if section_id == -1:
            transfer.section_id = None
            transfer.removed = 1
            transfer.reason = reason
            transfer.request_decision = None

            # Update section population
            sections_population = int(section_remove.population)
            section_remove.population = int(sections_population - 1)

            db.session.commit()

            result = 'warning'
            message = 'Student removed from class'

        else:
            transfer.section_id = section_id
            transfer.reassign = 1
            transfer.reason = reason

            # Update section population
            sections_population = int(section_transfer.population)
            section_transfer.population = int(sections_population + 1)

            sections_population = int(section_remove.population)
            section_remove.population = int(sections_population - 1)

            db.session.commit()

            result = 'success'
            message = 'Student successfully transferred!'

    return jsonify({'result': result, 'message': message})


@app.route('/request/action', methods=['POST'])
def request_action():
    result = ''
    message = ''
    section_id = int(request.form['section_id'])
    student_id = int(request.form['student_id'])
    action = int(request.form['action'])
    reason = str(request.form['reason'])

    student_req = db.session.query(Student).filter(Student.student_id == student_id).first()

    section_record = db.session.query(Section).filter(Section.section_id == section_id).first()

    if student_req is not None:
        student_req.request_decision = action

        # Request accept
        if action:
            student_req.section_id = section_id

            result = 'success'
            message = 'Request Approved!'

            section_record.population = int(section_record.population) + 1

            student_req.reason = None

        # Request declined
        else:
            result = 'success'
            message = 'Request Declined! Reason: ' + reason
            student_req.reason = reason

        student_req.request = None
        student_req.removed = 0
        student_req.reassign = None

        db.session.commit()
    else:
        result = 'danger'
        message = 'update failed'

    return jsonify({'result': result, 'message': message, 'action': action})


@app.route('/reassign/student', methods=['POST'])
def reassign_student():
    student_id = int(request.form['student_id'])

    student_reassign = db.session.query(Student).filter(Student.student_id == student_id).first()

    if student_reassign is not None:
        student_reassign.reassign = None
        db.session.commit()

        result = 'success'
        message = 'student reassigned'
    else:
        result = 'danger'
        message = 'update failed'

    return jsonify({'result': result, 'message': message})


@app.route('/save/grade', methods=['POST'])
def save_grade():
    result = 'success'
    message = 'grade saved'

    student_id = int(request.form['student_id'])
    student_grade = json.dumps(ave_grade)

    if not student_grade == '{}':
        result = 'success'
        message = 'grade saved'

        activity = Activity(
            date=datetime.datetime.now(),
            student_id=student_id,
            grade=student_grade
        )

        db.session.add(activity)
        db.session.commit()
    else:
        result = 'success'
        message = 'no grade saved'

    return jsonify({'result': result, 'message': message})


@app.route('/get/student/grade', methods=['GET'])
def get_studentGrade():
    arnis_poses = ["Left Temple Strike", "Right Temple Strike", "Left Shoulder Strike", "Right Shoulder Strike",
                   "Stomach Thrust", "Left Chest Thrust", "Right Chest Thrust", "Right Leg Strike",
                   "Left Leg Strike", "Left Eye Thrust", "Right Eye Thrust", "Crown Strike",
                   "Left Temple Block", "Right Temple Block", "Left Shoulder Block", "Right Shoulder Block",
                   "Stomach Thrust Block", "Left Chest Block", "Right Chest Block", "Right Leg Block",
                   "Left Leg Block", "Left Eye Block", "Right Eye Block", "Rising Block"]

    student_idq = request.args.get('student_id')

    result = ''
    student_name = ''
    activities = []
    average_grade = 0

    student_activity = db.session.query(Activity, Student, User)\
        .select_from(Activity)\
        .outerjoin(Student, Student.student_id == Activity.student_id)\
        .outerjoin(User, User.id == Student.user_id)\
        .filter(Student.student_id == student_idq).order_by(db.desc(Activity.date)).first()

    student = db.session.query(User, Student)\
        .select_from(User)\
        .outerjoin(Student, User.id == Student.user_id)\
        .filter(Student.student_id == student_idq).first()

    student_name = student[0].last_name + ', ' + student[0].first_name

    if student_activity:
        result = 'success'

        activities = student_activity[0].grade

        activities = json.loads(activities)

        activities = list(activities.values())

        average_grade = round(mean([int(x) for x in activities]), 2)

        arnis_poses = arnis_poses[:len(activities)]

        print(student_name, "\n", activities)

    return jsonify({'result': result, 'student_name': student_name, 'activities': activities,
                    'average_grade': average_grade, 'arnis_poses': arnis_poses})