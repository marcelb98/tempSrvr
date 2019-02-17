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

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators, BooleanField, HiddenField, ValidationError


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.Length(min=5)])

class NewPasswordForm(FlaskForm):
    user = HiddenField()
    password_old = PasswordField('Current password', [validators.Length(min=5)])
    password = PasswordField('Password', [validators.Length(min=5)])
    passwordv = PasswordField('Password verification', [validators.EqualTo('password', message='Passwords must match')])

    def validate_password_old(form, field):
        if form.user.data.check_password(field.data) is not True:
            raise ValidationError('Password is not correct.')

class NewUserForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.Length(min=5)])
    passwordv = PasswordField('Password verification', [validators.EqualTo('password', message='Passwords must match')])
    admin = BooleanField('Admin')

class VerifyActionForm(FlaskForm):
    verify = BooleanField('yes', [validators.DataRequired()])