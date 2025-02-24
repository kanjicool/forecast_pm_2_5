from flask import redirect, url_for, request, session, render_template
from flask_login import current_user, LoginManager, login_url, logout_user
from werkzeug.exceptions import Forbidden, Unauthorized
import datetime
from forecast_pm_2_5.models.users import User

from functools import wraps

login_manager = LoginManager()


def init_acl(app):
    login_manager.init_app(app)
    # principals.init_app(app)

    @app.errorhandler(401)
    def page_not_found(e):
        return unauthorized_callback()

    def no_permission(e):
        if login_manager.unauthorized_callback:
            return redirect(url_for("accounts.login"))
        return render_template("error_handler/403.html"), 403


def division_required(*divisions):
    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                raise Unauthorized()
            if hasattr(current_user, "division"):
                for division in divisions:
                    if division == current_user.division:
                        return func(*args, **kwargs)
            raise Forbidden()

        return wrapped

    return wrapper


def roles_required(*roles):
    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                raise Unauthorized()
            for role in roles:
                if role in current_user.roles:
                    return func(*args, **kwargs)
            raise Forbidden()

        return wrapped

    return wrapper


@login_manager.user_loader
def load_user(user_id):
    user = User.objects(id=user_id).first()
    return user


@login_manager.unauthorized_handler
def unauthorized_callback():
    if request.method == "GET":
        response = redirect(login_url("accounts.login", request.url))
        return response
    return redirect(url_for("accounts.login"))
