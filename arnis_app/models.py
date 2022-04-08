from flask_babelex import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserMixin
from arnis_app import app
from arnis_app.customClasses import NewUserManager


# Initialize Flask-BabelEx
babel = Babel(app)

# Initialize Flask-SQLAlchemy
db = SQLAlchemy(app)


# Define the User data-model that manages account
# NB: Make sure to add flask_user UserMixin !!!
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)

    # User information
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    last_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    first_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    middle_name = db.Column(db.String(100, collation='NOCASE'), nullable=True)
    gender = db.Column(db.String(10, collation='NOCASE'), nullable=False, server_default='')

    # User authentication information. The collation='NOCASE' is required
    # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
    email = db.Column(db.String(255, collation='NOCASE'), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    mobile = db.Column(db.String(100, collation='NOCASE'), nullable=False, unique=True)
    date_joined = db.Column(db.DateTime())  # Date registered
    email_confirmed_at = db.Column(db.DateTime())  # Date email confirmed

    # Define relationship with User table
    roles = db.relationship('Role', secondary='user_roles')
    teacher = db.relationship('Teacher')
    student = db.relationship('Student')
    pic = db.relationship('UserProfilePic')


# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


class UserRoles(db.Model):
    __tablename__ = 'user_roles'

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


# School Management tables
class Teacher(db.Model):
    __tablename__ = 'teachers'

    teacher_id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))

    # Define relationship with Section table
    section = db.relationship('Section')


class Student(db.Model):
    __tablename__ = 'students'

    student_id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    section_id = db.Column(db.Integer(), db.ForeignKey('sections.section_id', ondelete='CASCADE'))
    request = db.Column(db.Integer())
    request_decision = db.Column(db.Boolean(), nullable=True)
    reassign = db.Column(db.Integer())
    removed = db.Column(db.Boolean(), nullable=False, server_default='0')
    reason = db.Column(db.Text())

    # Define relationship with Activity & Video table
    activity = db.relationship('Activity')
    video = db.relationship('Video')


class Section(db.Model):
    __tablename__ = 'sections'

    section_id = db.Column(db.Integer(), primary_key=True)
    section_no = db.Column(db.Integer())
    teacher_id = db.Column(db.Integer(), db.ForeignKey('teachers.teacher_id', ondelete='CASCADE'))
    strand_id = db.Column(db.Integer(), db.ForeignKey('strands.strand_id', ondelete='CASCADE'))
    population = db.Column(db.Integer(), server_default='0')

    # Define relationship with Student table
    student = db.relationship('Student')


class Track(db.Model):
    __tablename__ = 'tracks'

    track_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255, collation='NOCASE'), nullable=False, server_default='')
    nickname = db.Column(db.String(50, collation='NOCASE'), nullable=False, server_default='')

    # Define relationship with Section table
    strands = db.relationship('Strand')


class Strand(db.Model):
    __tablename__ = 'strands'

    strand_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255, collation='NOCASE'), nullable=False, server_default='')
    nickname = db.Column(db.String(50, collation='NOCASE'), nullable=False, server_default='')
    track_id = db.Column(db.Integer(), db.ForeignKey('tracks.track_id', ondelete='CASCADE'))

    # Define relationship with Track table
    section = db.relationship('Section')


class Activity(db.Model):
    __tablename__ = 'activities'

    activity_id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.DateTime())
    student_id = db.Column(db.Integer(), db.ForeignKey('students.student_id', ondelete='CASCADE'))
    grade = db.Column(db.Text())


class Video(db.Model):
    __tablename__ = 'videos'

    video_id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.DateTime())
    filename = db.Column(db.Text(collation='NOCASE'), nullable=False)
    student_id = db.Column(db.Integer(), db.ForeignKey('students.student_id', ondelete='CASCADE'))
    grade = db.Column(db.Text())


class UserProfilePic(db.Model):
    __tablename__ = 'profile_pic'

    profile_id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    filename = db.Column(db.Text(collation='NOCASE'), nullable=False, server_default='profile_pic/def_profile.png')


def create_db():
    db.create_all()


def drop_db():
    db.drop_all()


def add_roles():
    role1 = Role(name='admin')
    role2 = Role(name='teacher')
    role3 = Role(name='student')

    db.session.add_all([role1, role2, role3])
    db.session.commit()


# call function for populating constant data to a table.
def insert_track():

    track = [i for i in range(4)]

    track_list = [
        ['Academic Track', 'ACAD'],
        ['Arts and Design Track', 'ARTS'],
        ['Sports Track', 'SPORTS'],
        ['Technological-Vocational Livelihood Track', 'TVL']
    ]

    for j in track:
        track[j] = Track(
            name=track_list[j][0],
            nickname=track_list[j][1]
        )

    strand = [i for i in range(24)]

    strand_list = [
        ['Accountancy, Business, and Management', 'ABM', 1],
        ['Science, Technology, Engineering and Mathematics', 'STEM', 1],
        ['Humanities and Social Science', 'HUMSS', 1],
        ['Animation', 'ANIM', 2],
        ['(Performing Art) Dance', 'DNC', 2],
        ['(Performing Art) Music', 'MSC', 2],
        ['(Performing Art) Theater Arts', 'THTR', 2],
        ['Film Production', 'PROD', 2],
        ['Sports Coaching', 'COACH', 3],
        ['Sports Officiating', 'OFFIC', 3],
        ['(Home Economics) Hotel and Restaurant Servicing', 'HRS', 4],
        ['(Home Economics) Tourism Servicing', 'TOUR', 4],
        ['(Home Economics) Food Production', 'FOOD', 4],
        ['(Home Economics) Health Care Services', 'HCS', 4],
        ['(Home Economics) Emergency Medical Services', 'EMS', 4],
        ['(ICT) Computer Programming', 'CMP', 4],
        ['(ICT) Computer System Servicing', 'CSS', 4],
        ['(ICT) Business Process Outsourcing', 'BPO', 4],
        ['(Industrial Arts) Drafting Technology', 'DRT', 4],
        ['(Industrial Arts) Automotive Servicing', 'AUTO', 4],
        ['(Industrial Arts) Electronic Products Assembly and Services', 'PAS', 4],
        ['(Industrial Arts) Electrical Installation and Maintenance', 'EIM', 4],
        ['(Industrial Arts) Construction Technology', 'CONST', 4],
        ['(Industrial Arts) Welding Technology', 'WELD', 4]
    ]

    for j in strand:
        strand[j] = Strand(
            name=strand_list[j][0],
            nickname=strand_list[j][1],
            track_id=strand_list[j][2]
        )

    db.session.add_all(track)
    db.session.add_all(strand)
    db.session.commit()


# Setup Flask-User and specify the User data-model
user_manager = NewUserManager(app, db, User)
