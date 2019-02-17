"""
    tempSrvr
    Copyright (C) 2019  Marcel Beyer

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
from datetime import datetime
import hashlib
from typing import List

from flask import Blueprint, request, abort

from model import Sensor, Value, db

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/v1/submit', methods=['POST'])
def show():
    sensor = request.values.get('sensor')
    time = request.values.get('time')
    temp = request.values.get('temp')
    signature = request.values.get('signature')

    if sensor == '' or time is None or temp is None or signature is None:
        return abort(400)

    try:
        sensor = int(sensor)
    except ValueError:
        return abort(400)

    s = Sensor.query.get(sensor)
    if s is None:
        return abort(404)

    if check_signature(s, signature, [str(sensor), time, temp]) is not True:
        return abort(403)

    try:
        time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return abort(400)

    try:
        temp = float(temp)
    except ValueError:
        return abort(400)

    value = Value(s, temp, time)
    db.session.add(value)
    db.session.commit()

    return "OK"

def check_signature(s:Sensor, signature:str, fields:List[str])->bool:
    """
    Check if the signature is correct for the given fields.

    :param s: The sensor which signed the data.
    :param signature: The signature sent by the sensor.
    :param fields: List of the fields which should be signed.
    :return: True if the signature was correct, False otherwise
    """
    sig = ''.join(fields) + s.api_key
    sig = hashlib.sha256(sig.encode('utf-8')).hexdigest()

    return sig == signature
