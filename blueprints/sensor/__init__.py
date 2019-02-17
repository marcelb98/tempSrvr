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

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required

import helpers
from blueprints.sensor.forms import NewSensorForm
from forms import VerifyActionForm
from helpers import require_admin
from model import Sensor, db

bp = Blueprint('sensor', __name__, url_prefix='/sensor')

@bp.route('/<id>')
def show(id:int):
    return "Sensor {}".format(id)

@bp.route('/manage')
@login_required
@require_admin
def manage():
    sensors = Sensor.query.all()
    return render_template('sensor/manage.html', sensors=sensors)

@bp.route('/manage/new', methods=['GET', 'POST'])
@login_required
@require_admin
def new():
    form = NewSensorForm()

    if form.validate_on_submit():
        # create sensor
        sensor = Sensor(form.name.data, form.public.data)
        db.session.add(sensor)
        db.session.commit()
        flash('Sensor was created successfully.','success')
        return redirect(url_for('sensor.manage'))

    return render_template('sensor/new.html', form=form)

@bp.route('/manage/<sensor>/newKey', methods=['GET', 'POST'])
@login_required
@require_admin
def new_key(sensor:int):
    sensor = Sensor.query.get(sensor)

    form = VerifyActionForm()

    if form.validate_on_submit() and form.verify.data is True:
        # reset API-Key
        password = helpers.gen_password(30)
        sensor.api_key = password
        db.session.add(sensor)
        db.session.commit()
        flash('Created new API-Key for sensor {} successfully.'.format(sensor.name), 'success')
        return redirect(url_for('sensor.manage'))

    return render_template('sensor/new_key.html', form=form, sensor=sensor)

@bp.route('/manage/<sensor>/delete', methods=['GET', 'POST'])
@login_required
@require_admin
def delete(sensor:int):
    sensor = Sensor.query.get(sensor)

    form = VerifyActionForm()

    if form.validate_on_submit() and form.verify.data is True:
        # delete sensor
        db.session.delete(sensor)
        db.session.commit()
        flash('{} was deleted successfully.'.format(sensor.name), 'success')
        return redirect(url_for('sensor.manage'))

    return render_template('sensor/delete.html', form=form, sensor=sensor)