from datetime import datetime
from arnis_app import app
from flask import render_template, request, redirect, url_for, flash
from arnis_app.models import db, user_manager, User, UserRoles, Role
from flask_login import current_user
from flask_user import login_required, roles_required, UserManager, UserMixin
from arnis_app.customClasses import NewUserManager
from wtforms.validators import ValidationError
from flask_user.translation_utils import gettext as _


@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        user_id = current_user.id
        tbl_role = Role.query.filter_by(id=user_id).first().name
        print(tbl_role)

        if tbl_role == 'teacher':
            return redirect(url_for('teacher_dashboard'))
        elif tbl_role == 'student':
            return redirect(url_for('student_dashboard'))
    return render_template("public/index.html", title='Index')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template("public/login.html", title='Login')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        filled = request.form
        user_email = filled['email']

        user = User.query.filter_by(email=user_email).first()
        if user:
            flash(_("User with email: '%(email)s' is already taken.", email=user_email), 'error')
            # raise ValidationError('That email is taken. Please choose a different one.')
        else:
            hashed_pass = user_manager.hash_password(filled['password'])
            role_num = 1 if filled['form_name'] == 'student' else 2
            user = User(
                last_name = filled['lname'],
                first_name = filled['fname'],
                middle_name = filled['mname'],
                gender = filled['sex'],
                email = filled['email'],
                password = hashed_pass,
                mobile = filled['pnum'],
                date_joined = datetime.now(),
                email_confirmed_at = datetime.now()
            )
            db.session.add(user)
            db.session.commit()

            user_role = UserRoles(
                user_id = user.id,
                role_id = role_num
            )
            db.session.add(user_role)
            db.session.commit()

            flash(_("You have successfully signed up!"), 'success')
            return redirect(url_for('login'))

    return render_template("public/signup.html", title='Signup')


@app.route('/about')
@roles_required('student')
def about():
    return render_template("public/about.html", title='About')