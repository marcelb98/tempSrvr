tempSrvr API
============
Since the sensors have to communicate with tempSrvr, they need an API access.
The intention of this file is to describe how the API works.

At the moment the only functionality provided by the API is receiving temperatures measured
by the sensors. Maybe this changes in future - feel free to create pull requests.

API requests should go to the URL ``/api/v<int>/<endpoint>``, where ``<int>`` has to be replaced
with the version number you want to use (e.g. ``1``). If a client wants to send a new temperature
using version 1 of the API to tempSrvr, it has to use the URL ``/api/v1/submit``.

UTF-8 is used as text encoding.

Receiving temperatures
----------------------
*New in API v1*

**Endpoint:** ``submit`` **Method:** POST

The client has to send a POST request with the following fields:

* sensor (the ID of the sensor)
* time (time the temperature was measured, YYYY-mm-dd HH:ii:ss, UTC)
* temp (measured temperature, degree Celsius)
* signature (signature over sensor, time and temp as described below)

The server will respond with one of the following codes:

* 201 Everything was ok, data was saved
* 404 The sensor (ID) is unknown to the server.
* 403 The signature was invalid.
* 400 Client sent a bad request (no correct data).
* 500 There were other errors.

Creating signatures
-------------------
Sometimes the server only accepts signed requests. In those cases the specification of the
endpoint defines over which fields this signature has to be calculated.

Calculating the signature is easy: just concatenate the values of the fields requested to sign
(it's important to keep the order in which the fields are named in the specification).
Then concatenate this string with the API-Key of the sensor and calculate a SHA256-Hash (hex digest).
This hash is the signature.