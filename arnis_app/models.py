from flask_babelex import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserMixin
from arnis_app import app
from .customClasses import NewUserManager


# Initialize Flask-BabelEx
babel = Babel(app)

# Initialize Flask-SQLAlchemy
db = SQLAlchemy(app)


# Define the User data-model that manages account
# NB: Make sure to add flask_user UserMixin !!!
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    # User information
    last_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    first_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    middle_name = db.Column(db.String(100, collation='NOCASE'), nullable=True, server_default='')
    gender = db.Column(db.String(10, collation='NOCASE'), nullable=False, server_default='')

    # User authentication information. The collation='NOCASE' is required
    # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
    email = db.Column(db.String(255, collation='NOCASE'), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    mobile = db.Column(db.String(20, collation='NOCASE'), nullable=False, unique=True)
    date_joined = db.Column(db.DateTime())  # Date registered
    email_confirmed_at = db.Column(db.DateTime())  # Date email confirmed
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.role_id', ondelete='CASCADE'))

    # Define relationship with User table
    roles = db.relationship('Role')
    teacher = db.relationship('Teacher')
    student = db.relationship('Student')


# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'roles'

    role_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20), unique=True)

    # Back propagates relationship to User table
    user = db.relationship('User')


# School Management tables
class Teacher(db.Model):
    __tablename__ = 'teachers'

    teacher_id = db.Column(db.Integer(), primary_key=True)
    id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))

    # Define relationship with Section table
    section = db.relationship('Section')


class Student(db.Model):
    __tablename__ = 'students'

    student_id = db.Column(db.Integer(), primary_key=True)
    id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
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
    grade = db.Column(db.Float())


class Video(db.Model):
    __tablename__ = 'videos'

    video_id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.DateTime())
    filename = db.Column(db.String(512, collation='NOCASE'), nullable=False)
    student_id = db.Column(db.Integer(), db.ForeignKey('students.student_id', ondelete='CASCADE'))
    grade = db.Column(db.Float())


# Setup Flask-User and specify the User data-model
user_manager = NewUserManager(app, db, User)