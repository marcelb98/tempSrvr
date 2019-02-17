import functools
from urllib.parse import urlparse, urljoin

from flask import request, abort
from flask_login import current_user

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
