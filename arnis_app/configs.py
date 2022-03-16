import os


class ConfigClass(object):
    """ Flask application config """

    # Flask settings
    SECRET_KEY = str(os.urandom(24))

    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.sqlite'  # File-based SQL database
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Avoids SQLAlchemy warning

    # Flask-Mail SMTP server settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'projectaraw2022@gmail.com'
    MAIL_PASSWORD = '**ThesisNilaElias@Jeah**'
    MAIL_DEFAULT_SENDER = '"Project ARAW" <noreply@araw.com>'

    USER_ENABLE_REMEMBER_ME = False

    # Flask-User settings
    USER_APP_NAME = "Project ARAW: A Real-time Arnis Web-application"  # Shown in and email templates and page footers

    # Allow users to login and register with an email address & enable email authentication
    USER_ENABLE_EMAIL = True
    USER_ENABLE_USERNAME = False  # Disable username authentication
    USER_EMAIL_SENDER_NAME = USER_APP_NAME
    USER_EMAIL_SENDER_EMAIL = "noreply@araw.com"

    USER_SHOW_EMAIL_DOES_NOT_EXIST = True

    USER_LOGIN_URL = '/login'  # URL route to register
    USER_LOGIN_TEMPLATE = 'public/login.html'  # Login template/html used

    USER_FORGOT_PASSWORD_URL = '/forgot-password'
    USER_FORGOT_PASSWORD_TEMPLATE = 'public/forgot_password.html'

    # USER_REGISTER_URL = '/signup'  # URL route to register
    # USER_REGISTER_TEMPLATE = 'public/signup.html'  # Register template/html used

    # Redirect to after an action
    USER_AFTER_LOGOUT_ENDPOINT = 'index'  # Redirect to home page if user logs out
    USER_AFTER_FORGOT_PASSWORD_ENDPOINT = 'login'  # Redirect to login page after requested to reset password