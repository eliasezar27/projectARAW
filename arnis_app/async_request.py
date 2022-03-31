from arnis_app.models import db, User, Teacher, Section, Strand, Track, Student
from flask import request, jsonify
from arnis_app import app
from flask_login import current_user


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
        .order_by(db.desc('counts'))\
        .all()

    sectionCounts = dict(sectionCounts)
    labels = list(sectionCounts.keys())

    return jsonify({'result': 'result!', 'sectionCounts': sectionCounts, 'labels': labels})


@app.route('/section/count/perTrack', methods=['GET'])
def get_sectionCountPerTrack():

    user_id = current_user.id

    # Query number of sections per Track handled by a teacher
    sectionCounts = db.session.query(Track.nickname, db.func.count(Section.track_id).label('counts')) \
        .select_from(Track) \
        .outerjoin(Section, Track.track_id == Section.track_id) \
        .outerjoin(Teacher, Teacher.teacher_id == Section.teacher_id) \
        .filter(Teacher.user_id == user_id)\
        .group_by(Track.nickname) \
        .group_by(Section.track_id.label('counts')) \
        .order_by(db.desc('counts')) \
        .all()

    sectionCounts = dict(sectionCounts)
    track_names = list(dict(db.session.query(Track.track_id, Track.nickname).select_from(Track).all()).values())
    labels = list(sectionCounts.keys())

    for i in track_names:
        if not(i in labels):
            labels.append(i)

    return jsonify({'result': 'result!', 'sectionCounts': sectionCounts, 'labels': labels})