"""
    tempSrvr
    Copyright (C) 2018  Marcel Beyer

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from flask import Blueprint, render_template, flash, request, abort, redirect, url_for, Markup
from flask_login import LoginManager, login_user, login_required, logout_user

import helpers
from helpers import is_safe_url, require_admin
from blueprints.user.forms import LoginForm, VerifyActionForm, NewUserForm
from model import User, db

bp = Blueprint('user', __name__, url_prefix='/user')

login_manager = LoginManager()
login_manager.login_view = "user.login"
login_manager.login_message = "Please log in to access this page."

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.check_password(form.password.data) is True:
            login_user(user)

            next = request.args.get('next')
            if not is_safe_url(next):
                return abort(400)
            return redirect(next or url_for('home'))
        else:
            flash('Invalid login!', 'danger')
    return render_template('user/login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Successfully logged out.')
    return redirect(url_for('home'))

@bp.route('/settings')
@login_required
def settings():
    return "settings"

@bp.route('/manage')
@login_required
@require_admin
def manage():
    users = User.query.all()
    return render_template('user/manage.html', users=users)

@bp.route('/new', methods=['GET','POST'])
@login_required
@require_admin
def new():
    form = NewUserForm()

    if form.validate_on_submit():
        user = User(form.username.data, form.password.data)
        if form.admin.data is True:
            user.admin = True
        db.session.add(user)
        db.session.commit()
        flash('User was created successfully.', 'success')
        redirect(url_for('user.manage'))

    return render_template('user/new.html', form=form)

@bp.route('/manage/<user>/passwordreset', methods=['GET', 'POST'])
@login_required
@require_admin
def password_reset(user:int):
    user = User.query.get(user)

    form = VerifyActionForm()

    if form.validate_on_submit() and form.verify.data is True:
        # reset password
        password = helpers.gen_password()
        user.setPassword(password)
        db.session.add(user)
        db.session.commit()
        flash('Password for {} was changed successfully.'.format(user.username), 'success')
        flash(Markup('The new password is: <tt>{}</tt>'.format(password)), 'info')
        return redirect(url_for('user.manage'))

    return render_template('user/password_reset.html', form=form, user=user)

@bp.route('/manage/<user>/delete', methods=['GET', 'POST'])
@login_required
@require_admin
def delete(user:int):
    user = User.query.get(user)

    form = VerifyActionForm()

    if form.validate_on_submit() and form.verify.data is True:
        # delete user
        db.session.delete(user)
        db.session.commit()
        flash('{} was deleted successfully.'.format(user.username), 'success')
        return redirect(url_for('user.manage'))

    return render_template('user/delete.html', form=form, user=user)