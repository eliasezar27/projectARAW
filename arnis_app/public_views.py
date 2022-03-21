from datetime import datetime
from arnis_app import app
from flask import render_template, request, redirect, url_for, flash
from arnis_app.models import db, user_manager, User, UserRoles, Role, Teacher, Student, UserProfilePic
from flask_login import current_user
# from flask_user import current_user, login_required, roles_required, UserManager, UserMixin
# from arnis_app.customClasses import NewUserManager
# from wtforms.validators import ValidationError
from flask_user.translation_utils import gettext as _


@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        user_id = current_user.id
        role_num = UserRoles.query.filter_by(user_id=user_id).order_by(UserRoles.role_id).first().role_id
        role_name = Role.query.filter_by(id=role_num).first().name

        if role_name == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif role_name == 'teacher':
            return redirect(url_for('teacher_dashboard'))
        elif role_name == 'student':
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
        pnum = filled['pnum']
        entity_role = str(filled['form_name'])

        user = User.query.filter_by(email=user_email).first()
        mobile = User.query.filter_by(mobile=pnum).first()
        if user:
            # Raises a flash if email is already in used.
            flash(_("User with email: '%(email)s' is already taken.", email=user_email), 'error')
        elif mobile:
            # Raises a flash if mobile number is already in used.
            flash(_("'%(phone)s' is already registered to an account.", phone=pnum), 'error')
        else:
            hashed_pass = user_manager.hash_password(filled['password'])
            role_num = 2 if filled['form_name'] == 'teacher' else 3

            # Insert signup data from fields to each Uer attribute
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

            # Get User id of recently committed data to User table
            user_id = user.id

            # Insert User id with the user's corresponding Role id to the UserRole table
            user_role = UserRoles(
                user_id = user_id,
                role_id = role_num
            )

            # Insert User id to the user's position based on user's role
            position = None
            if role_num == 2:
                position = Teacher(
                    user_id = user_id
                )
            elif role_num == 3:
                position = Student(
                    user_id = user_id
                )

            # Insert default user's profile picture
            profile_pic = UserProfilePic(
                user_id = user_id
            )

            db.session.add_all([user_role, position, profile_pic])
            db.session.commit()

            flash(_("You have successfully signed up as a '" + entity_role + "'!"), 'success')
            return redirect(url_for('login'))

    return render_template("public/signup.html", title='Signup')


@app.route('/about')
def about():
    return render_template("public/about.html", title='About')