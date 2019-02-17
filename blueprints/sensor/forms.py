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
from wtforms import StringField, validators, BooleanField, ValidationError, DateTimeField

from model import Sensor


class NewSensorForm(FlaskForm):
    name = StringField('Name', [validators.Length(min=4, max=25)])
    public = BooleanField('Public sensor?')

    def validate_name(form, field):
        if Sensor.query.filter_by(name=field.data).count() > 0:
            raise ValidationError("There's already a sensor with this name.")

class ShowIntervalForm(FlaskForm):
    start = DateTimeField('Start', [validators.DataRequired()], format='%Y-%m-%d %H:%M:%S')
    end = DateTimeField('End', [validators.DataRequired()], format='%Y-%m-%d %H:%M:%S')