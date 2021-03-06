import functools
from urllib.parse import urlparse, urljoin

from flask import request, abort
from flask_login import current_user

from dominate import tags
from flask_nav.renderers import Renderer


# http://flask.pocoo.org/snippets/62/
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


def require_admin(f):
    """
    Require that the logged in user has admin permissions.
    If the user has no admin permissions, a 403 error will be returned.
    """

    @functools.wraps(f)
    def decorator(*args, **kwargs):
        if current_user.admin is not True:
            abort(403)
        return f(*args, **kwargs)

    return decorator

def require_sensor_permission(f):
    """
    Check if the current user (which may be logged in or not) has the permission to view data of this sensor.
    This will be the case if a) the sensor is public or b) the user has been granted access to the sensor by an admin.

    If the user has no permissions, a 403 error will be returned.
    """

    @functools.wraps(f)
    def decorator(*args, **kwargs):
        from model import Sensor
        sensor = Sensor.query.get(kwargs['id'])
        if sensor is None:
            return abort(404)
        if sensor.public is True:
            pass
        else:
            if current_user.is_authenticated is False or sensor not in current_user.sensors:
                abort(403)
        return f(*args, **kwargs)

    return decorator


def gen_password(len: int = 10):
    """
    Generate a random password.
    :param len: Length of the password.
    :return: The generated password
    """

    import random
    import string
    choices = []
    for i in range(0,len):
        choices.append(random.choice(string.ascii_letters + string.digits))
    return ''.join(choices)


class IconText():
    """
    Workaround to store title and icon for items in flask-nav.
    """

    def __init__(self, text: str, icon: str = 'square'):
        self.text = text
        self.icon = icon


class BootstrapNavRenderer(Renderer):
    def visit_Navbar(self, node):
        sub = []
        for item in node.items:
            sub.append(self.visit(item))

        return tags.ul(cls='nav flex-column', *sub)

    def visit_View(self, node):
        active = 'active' if node.active else ''
        return tags.li(
            tags.a(tags.span(data_feather=node.text.icon), node.text.text, href=node.get_url(),
                   cls='nav-link {}'.format(active)),
            cls='nav-item'
        )
