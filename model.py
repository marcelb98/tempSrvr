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

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash

from helpers import gen_password

db = SQLAlchemy()

# helper table for User-Sensor many-to-many relationship
# (defining which user is allowed to view temperatures of which sensors if they're not public)
sensor_permission = db.Table('view_permission',
    db.Column('sensor_id', db.Integer, db.ForeignKey('sensor.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    """
    Users which are using the system.
    Admins (admin=True) are allowed to manage the system (e.g. create sensors).
    Normal users are only allowed to view the data of restricted sensors.
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    admin = db.Column(db.Boolean, default=False, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    passwort = db.Column(db.String)

    sensors = db.relationship('Sensor', secondary=sensor_permission, lazy='subquery',
                           backref=db.backref('users', lazy=True))

    def __init__(self, username, password):
        self.username = username
        self.setPassword(password)

    def setPassword(self, password):
        self.passwort = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passwort, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Sensor(db.Model):
    """
    A sensor for which temperatures are collected.
    """
    __tablename__ = 'sensor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    public = db.Column(db.Boolean, default=False) # defines if temperatures of this sensor are public
    api_key = db.Column(db.String, nullable=False)

    values = db.relationship("Value", back_populates="sensor", lazy="dynamic")

    def __init__(self, name:str, public:bool):
        self.name = name
        self.public = public
        self.api_key = gen_password(30)

    def __str__(self):
        return self.name

class Value(db.Model):
    """
    The temperatures meassured.
    Times are saved in UTC.
    """
    __tablename__ = 'value'
    id = db.Column(db.Integer, primary_key=True)
    temp = db.Column(db.Float, nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'), nullable=False)
    sensor = db.relationship("Sensor", back_populates="values")

    def __init__(self, sensor, temp, time=None):
        self.sensor_id = sensor.id
        self.time = datetime.datetime.utcnow() if time is None else time
        self.temp = temp
