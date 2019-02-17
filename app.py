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

from flask import Flask, redirect, url_for, render_template, request
from flask_login import current_user

from flask_migrate import Migrate
from flask_nav import Nav, register_renderer
from flask_nav.elements import View, Navbar

from config import Config
import model
from model import Sensor
from forms import RegistrationForm
from helpers import BootstrapNavRenderer, IconText

from blueprints import sensor, user
from blueprints.user import login_manager

nav = Nav()

def create_app():
    app = Flask(__name__)
    app.secret_key = Config.secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.database_url
    app.app_context()

    login_manager.init_app(app)

    app.register_blueprint(sensor.bp)
    app.register_blueprint(user.bp)

    register_renderer(app, 'bootstrap', BootstrapNavRenderer)

    return app

app = create_app()
app.app_context().push()
nav.init_app(app)

with app.app_context():
    model.db.init_app(app)

migrate = Migrate(app, model.db)

def get_app():
    global app
    return app

if __name__ == '__main__':
    app.run()

@app.context_processor
def sensors():
    return dict(sensors=Sensor.query.filter_by(public=True).all())

@nav.navigation()
def main_nav():
    items = [
        View(IconText('Home','home'), 'home')
    ]

    # add public sensors
    for sensor in Sensor.query.filter_by(public=True).all():
        items.append(View(IconText(sensor.name,'thermometer'), 'sensor.show', id=sensor.id))

    # add private sensors

    # add admin stuff
    if current_user.is_authenticated and current_user.admin is True:
        items.append(View(IconText('Manage users','users'), 'user.manage'))

    # add stuff for logged in users
    if current_user.is_authenticated:
        items.append(View(IconText('Settings','settings'), 'user.settings'))

    return Navbar('', *items)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/install', methods=['GET', 'POST'])
def install():
    if len(model.User.query.all()) > 0:
        return redirect(url_for('home'))

    form = RegistrationForm(request.form)

    if request.method == 'POST' and form.validate():
        # register user
        admin = model.User(form.username.data, form.password.data)
        admin.admin = True
        model.db.session.add(admin)
        model.db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('install/admin.html', form=form)

