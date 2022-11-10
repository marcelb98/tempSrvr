tempSrvr
========
tempSrvr is a web application thought to show measured temperature
values submitted by sensors via HTTP.

It's possible to declare sensors as public, so that everybody can see the temperatures.
All other sensors are limited to a specified set of users. To see those temperatures the
users have to log in.

New temperatures are submitted through the API. If you're looking for a client,
take a look at `piTemp <https://github.com/marcelb98/piTemp>`_.

Config
------
By default config is read from the `config.py` in the projects main directory.
If the environment variable `CONFIGFILE` is provided, the config file will be read from the path stated in this variable.

