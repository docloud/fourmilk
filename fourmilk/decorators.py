# coding=utf8

import functools
from jsonpickle import dumps
from flask import (
    jsonify as flask_jsonify
)
from webargs.flaskparser import use_args as flask_useargs
from werkzeug.wrappers import Response

JSON_TYPES = (str, unicode, int, float, list)


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
    def _deco(func):
        func.args = argmap
        _base_deco = flask_useargs(argmap, req, locations,
                                   as_kwargs, validate)
        return _base_deco(func)
    return _deco