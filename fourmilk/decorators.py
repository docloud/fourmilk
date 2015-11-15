# coding=utf8

import functools
from datetime import timedelta

from jsonpickle import dumps
from flask import (
    jsonify as flask_jsonify,
    make_response,
    request,
    current_app
)
from webargs.flaskparser import use_args as flask_useargs
from werkzeug.wrappers import Response

JSON_TYPES = (str, unicode, int, float, list, type(None))


def decorator(caller):
    " Implement like decorator.decorator "

    @functools.wraps(caller)
    def _deco(func):
        # Decorator generator.
        @functools.wraps(func)
        def _wraps(*args, **kwargs):
            return caller(func, *args, **kwargs)

        return _wraps

    return _deco


@decorator
def jsonify(func, *args, **kwargs):
    """Creates a :class:`~flask.Response` with the JSON representation of
    the given arguments with an `application/json` mimetype.  The arguments
    to this function are the same as to the :class:`dict` constructor.

    It is a decorator for :func:`flask.jsonify`, to auto serialize object or
    dictionary to json response by :module:`jsonpickle` & :func:`flask.jsonify`

    Example usage::

        from flask.views import MethodView
        from .decorator import jsonify

        class User(object):
            def __init__(self, name):
                self.name = name


        class UserView(MethodView):
            decorators = [jsonify]

            def get(self):
                return {"name": "Tony"}

            def post(self):
                user = User("Tony")
                return user

    This will send a JSON response like this to the browser::

        {
            "name": "Tony",
        }

    For security reasons only objects are supported toplevel.  For more
    information about this, have a look at :ref:`json-security`.

    This function's response will be pretty printed if it was not requested
    with ``X-Requested-With: XMLHttpRequest`` to simplify debugging unless
    the ``JSONIFY_PRETTYPRINT_REGULAR`` config parameter is set to false.
    """
    result = func(*args, **kwargs)

    if isinstance(result, dict):
        pass
    elif isinstance(result, Response):
        return result
    elif type(result) in JSON_TYPES:
        result = {"data": result}
    else:
        result = dumps(result, unpicklable=False)

    return flask_jsonify(result)


def router(rule, **options):
    def _deco(func):
        func.rule = rule
        func.options = options
        return func

    return _deco


def use_args(argmap, req=None, locations=None,
             as_kwargs=False, validate=None, **kwargs):
    """Decorator that injects parsed arguments into a view function or method.

    It is a wrapper for :func:`webargs.flaskparser.use_args`

    Example usage:

    .. code-block:: python

        @router('/echo', methods=['get', 'post'])
        @use_args({'name': fields.Str()})
        def greet(args):
            return 'Hello ' + args['name']

    :param argmap: Either a `marshmallow.Schema`, a `dict`
        of argname -> `marshmallow.fields.Field` pairs, or a callable
        which accepts a request and returns a `marshmallow.Schema`.
    :param tuple locations: Where on the request to search for values.
    :param bool as_kwargs: Whether to insert arguments as keyword arguments.
    :param callable validate: Validation function that receives the dictionary
        of parsed arguments. If the function returns ``False``, the parser
        will raise a :exc:`ValidationError`.
    """
    def _deco(func):
        func.args = argmap
        _base_deco = flask_useargs(argmap, req, locations,
                                   as_kwargs, validate)
        return _base_deco(func)

    return _deco


def use_kwargs(*args, **kwargs):
    """Decorator that injects parsed arguments into a view function or method
        as keyword arguments.

        This is a shortcut to :meth:`use_args` with ``as_kwargs=True``.

        Example usage with Flask: ::

        .. code-block:: python

            @router('/echo', methods=['get', 'post'])
            @use_kwargs({'name': fields.Str()})
            def greet(name):
                return 'Hello ' + name

    Receives the same ``args`` and ``kwargs`` as :meth:`use_args`.
    """
    kwargs['as_kwargs'] = True
    return use_args(*args, **kwargs)


def crossdomain(origin=None, methods=None, headers=None, expose_headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True, credentials=False):
    """
    http://flask.pocoo.org/snippets/56/
    """
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if expose_headers is not None and not isinstance(expose_headers, str):
        expose_headers = ', '.join(x.upper() for x in expose_headers)
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if credentials:
                h['Access-Control-Allow-Credentials'] = 'true'
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            if expose_headers is not None:
                h['Access-Control-Expose-Headers'] = expose_headers
            return resp

        return functools.update_wrapper(wrapped_function, f)
    return decorator