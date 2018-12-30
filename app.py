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

from flask import Flask

from flask_migrate import Migrate

from config import Config
import model

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

@app.route('/')
def hello_world():
    return 'Hello World!'



