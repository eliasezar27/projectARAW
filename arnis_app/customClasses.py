from flask_user import UserManager, user_manager__views, user_manager__settings, user_manager__utils
from flask import current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from flask_user import signals
from flask_user.translation_utils import gettext as _
from urllib.parse import quote, unquote
from datetime import datetime


# Custom user_manager__views
class NewViews(user_manager__views.UserManager__Views):

    def __init__(self):
        super().__init__()

    def login_view(self):
        """Prepare and process the login form."""
        if current_user.is_authenticated:
            return redirect(url_for('index'))

        # Authenticate username/email and login authenticated users.

        safe_next_url = self._get_safe_next_url('next', self.USER_AFTER_LOGIN_ENDPOINT)
        safe_reg_next = self._get_safe_next_url('reg_next', self.USER_AFTER_REGISTER_ENDPOINT)

        # Immediately redirect already logged in users
        if self.call_or_get(current_user.is_authenticated) and self.USER_AUTO_LOGIN_AT_LOGIN:
            return redirect(safe_next_url)

        # Initialize form
        login_form = self.LoginFormClass(request.form)  # for login.html
        register_form = self.RegisterFormClass()  # for login_or_register.html
        if request.method != 'POST':
            login_form.next.data = register_form.next.data = safe_next_url
            login_form.reg_next.data = register_form.reg_next.data = safe_reg_next

        # Process valid POST
        if request.method == 'POST' and login_form.validate():
            # Retrieve User
            user = None
            user_email = None
            if self.USER_ENABLE_USERNAME:
                # Find user record by username
                user = self.db_manager.find_user_by_username(login_form.username.data)

                # Find user record by email (with form.username)
                if not user and self.USER_ENABLE_EMAIL:
                    user, user_email = self.db_manager.get_user_and_user_email_by_email(login_form.username.data)
            else:
                # Find user by email (with form.email)
                user, user_email = self.db_manager.get_user_and_user_email_by_email(login_form.email.data)

            if user:
                # Log user in
                safe_next_url = self.make_safe_url(login_form.next.data)
                return self._do_login_user(user, safe_next_url, login_form.remember_me.data)

        # Render form
        self.prepare_domain_translations()
        template_filename = self.USER_LOGIN_AUTH0_TEMPLATE if self.USER_ENABLE_AUTH0 else self.USER_LOGIN_TEMPLATE
        return render_template(template_filename,
                      form=login_form,
                      login_form=login_form,
                      register_form=register_form)

    def logout_view(self):
        """Process the logout link."""
        """ Sign the user out."""

        # Send user_logged_out signal
        signals.user_logged_out.send(current_app._get_current_object(), user=current_user)

        # Use Flask-Login to sign out user
        logout_user()

        # Flash a system message
        flash(_('You have signed out successfully.'), 'success')

        # Redirect to logout_next endpoint or '/'
        safe_next_url = self._get_safe_next_url('next', self.USER_AFTER_LOGOUT_ENDPOINT)
        return redirect(safe_next_url)

    def forgot_password_view(self):
        """Prompt for email and send reset password email."""

        # Initialize form
        form = self.ForgotPasswordFormClass(request.form)

        # Process valid POST
        if request.method == 'POST' and form.validate():
            # Get User and UserEmail by email
            email = form.email.data
            user, user_email = self.db_manager.get_user_and_user_email_by_email(email)

            if user and user_email:
                # Send reset_password email
                self.email_manager.send_reset_password_email(user, user_email)

                # Send forgot_password signal
                signals.user_forgot_password.send(current_app._get_current_object(), user=user)

            # Flash a system message
            flash(_(
                "A reset password email has been sent to '%(email)s'. Open that email and follow the instructions to "
                "reset your password.",
                email=email), 'success')

            # Redirect to the login page
            return redirect(self._endpoint_url(self.USER_AFTER_FORGOT_PASSWORD_ENDPOINT))

        elif form.email.data is not None:

            flash(_(
                "User with email: '%(email)s' is not registered to this platform.",
                email=form.email.data), 'error')

        # Render form
        self.prepare_domain_translations()
        return render_template(self.USER_FORGOT_PASSWORD_TEMPLATE, form=form)


# Custom UserManager class
class NewUserManager(UserManager, NewViews):
    def __init__(self, app, db, UserClass, **kwargs):
        super().__init__(app, db, UserClass, **kwargs)