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
import datetime

from flask import Blueprint, render_template, flash, redirect, url_for, request, abort
from flask_login import login_required
from sqlalchemy import and_

import helpers
from blueprints.sensor.forms import NewSensorForm, ShowIntervalForm
from forms import VerifyActionForm, MultiCheckboxForm
from helpers import require_admin, require_sensor_permission
from model import Sensor, db, User, Value

bp = Blueprint('sensor', __name__, url_prefix='/sensor')


@bp.route('/<id>')
@require_sensor_permission
def show(id: int):
    sensor = Sensor.query.get(id)

    form = ShowIntervalForm(request.args, csrf_enabled=False)
    if form.start.data is None: form.start.data = datetime.datetime.utcnow() - datetime.timedelta(days=3)
    if form.end.data is None: form.end.data = datetime.datetime.utcnow()

    # newest temperature
    temp = sensor.values.order_by(Value.time.desc()).first()

    temps = sensor.values.order_by(Value.time.asc()).filter(
        and_(Value.time >= form.start.data, Value.time <= form.end.data)).all()

    values = {'xs': [], 'ys': []}
    for temp in temps:
        values['xs'].append(temp.time)
        values['ys'].append(temp.temp)

    return render_template('sensor/show.html', form=form, sensor=sensor, temp=temp, values=values)


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
        flash('Sensor was created successfully.', 'success')
        return redirect(url_for('sensor.manage'))

    return render_template('sensor/new.html', form=form)


@bp.route('/manage/<sensor>/newKey', methods=['GET', 'POST'])
@login_required
@require_admin
def new_key(sensor: int):
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
def delete(sensor: int):
    sensor = Sensor.query.get(sensor)

    form = VerifyActionForm()

    if form.validate_on_submit() and form.verify.data is True:
        # delete sensor
        db.session.delete(sensor)
        db.session.commit()
        flash('{} was deleted successfully.'.format(sensor.name), 'success')
        return redirect(url_for('sensor.manage'))

    return render_template('sensor/delete.html', form=form, sensor=sensor)


@bp.route('/manage/<sensor>/users', methods=['GET', 'POST'])
@login_required
@require_admin
def user_permissions(sensor: int):
    from wtforms import BooleanField

    sensor = Sensor.query.get(sensor)
    if sensor.public:
        flash('The selected sensor is a public sensor', 'info')
        return redirect(url_for('sensor.manage'))

    FieldList = [
        # ("Field-Name",BooleanField('Text')),
    ]

    users = User.query.all()
    for user in users:
        active = True if sensor in user.sensors else False
        FieldList.append((str(user.id), BooleanField(user.username, default=active)))

    class F(MultiCheckboxForm):
        pass

    for (name, field) in FieldList:
        setattr(F, name, field)
    form = F()

    if form.validate_on_submit():
        for user in users:
            if form._fields[str(user.id)].data is True:
                # user should have access
                user.sensors.append(sensor)
            elif sensor in user.sensors:
                # users access has to be removed
                user.sensors.remove(sensor)
            db.session.add(user)
        db.session.commit()
        flash('Updated user permissions successfully.', 'success')
        return redirect(url_for('sensor.manage'))

    return render_template('sensor/user_permissions.html', form=form, sensor=sensor)
