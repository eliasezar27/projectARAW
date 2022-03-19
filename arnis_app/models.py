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
    middle_name = db.Column(db.String(100, collation='NOCASE'), nullable=True, server_default='')
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

    # Define relationship with Activity & Video table
    activity = db.relationship('Activity')
    video = db.relationship('Video')


class Section(db.Model):
    __tablename__ = 'sections'

    section_id = db.Column(db.Integer(), primary_key=True)
    teacher_id = db.Column(db.Integer(), db.ForeignKey('teachers.teacher_id', ondelete='CASCADE'))
    track_id = db.Column(db.Integer(), db.ForeignKey('tracks.track_id', ondelete='CASCADE'))
    strand_id = db.Column(db.Integer(), db.ForeignKey('strands.strand_id', ondelete='CASCADE'))
    population = db.Column(db.Integer())

    # Define relationship with Student table
    student = db.relationship('Student')


class Track(db.Model):
    __tablename__ = 'tracks'

    track_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255, collation='NOCASE'), nullable=False, server_default='')

    # Define relationship with Section table
    section = db.relationship('Section')


class Strand(db.Model):
    __tablename__ = 'strands'

    strand_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255, collation='NOCASE'), nullable=False, server_default='')

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
        'Academic Track',
        'Arts and Design Track',
        'Sports Track',
        'Technological-Vocational Livelihood Track'
    ]

    for j in track:
        track[j] = Track(
            name=track_list[j]
        )

    strand = [i for i in range(24)]

    strand_list = [
        'Accountancy, Business, and Management',
        'Science, Technology, Engineering and Mathematics',
        'Humanities and Social Science',
        'Animation',
        '(Performing Art) Dance',
        '(Performing Art) Music',
        '(Performing Art) Theater Arts',
        'Film Production',
        'Sports Coaching',
        'Sports Officiating',
        '(Home Economics) Hotel and Restaurant Servicing',
        '(Home Economics) Tourism Servicing',
        '(Home Economics) Food Production',
        '(Home Economics) Health Care Services',
        '(Home Economics) Emergency Medical Services',
        '(ICT) Computer Programming',
        '(ICT) Computer System Servicing',
        '(ICT) Business Process Outsourcing',
        '(Industrial Arts) Drafting Technology',
        '(Industrial Arts) Automotive Servicing',
        '(Industrial Arts) Electronic Products Assembly and Services',
        '(Industrial Arts) Electrical Installation and Maintenance',
        '(Industrial Arts) Construction Technology',
        '(Industrial Arts) Welding Technology'
    ]

    for j in strand:
        strand[j] = Strand(
            name=strand_list[j]
        )

    db.session.add_all(track)
    db.session.add_all(strand)
    db.session.commit()


# Setup Flask-User and specify the User data-model
user_manager = NewUserManager(app, db, User)
