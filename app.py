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

from flask_migrate import Migrate

from config import Config
import model
from forms import RegistrationForm


def create_app():
    app = Flask(__name__)
    app.secret_key = Config.secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.database_url
    app.app_context()
    return app

app = create_app()
app.app_context().push()

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
    return dict(sensors=['a'])

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

