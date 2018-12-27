from flask import Blueprint, render_template, redirect, request
from flask_login import LoginManager, login_required, logout_user

from app.specs import mappings
from app.handlers import *
from app.utils import to_single_dict

bp = Blueprint('base_bp', __name__)

login_manager = LoginManager()
login_manager.login_view = "base_bp.login"
login_manager.user_callback = handle_user_loading

# TODO Deprecate
login_key_mappings = mappings.login['key_mappings']


@bp.route("/")
@login_required
def main():
    return render_template('index.html')


@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', **login_key_mappings)
    elif request.method == 'POST':
        result = handle_register(**to_single_dict(request.form))
        if result.success:
            return redirect("/")
        else:
            return render_template('register.html', err_msg=result.view_message, **login_key_mappings)


@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html', **login_key_mappings)
    elif request.method == "POST":
        result = handle_login(**to_single_dict(request.form))
        if result.success:
            return redirect("/")
        else:
            return render_template('login.html', err_msg=result.view_message, **login_key_mappings)


@bp.route("/logout", methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('/')
