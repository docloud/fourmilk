# coding=utf8

import functools
from jsonpickle import dumps
from flask import (
    Flask,
    jsonify as flask_jsonify
)

JSON_TYPES = (str, unicode, int, float)


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

    if type(result) is dict:
        pass
    elif type(result) in JSON_TYPES:
        result = {"data": result}
    else:
        result = dumps(result, unpicklable=False)

    print(result)
    return flask_jsonify(result)


def router(rule, **options):
    def _deco(func):
        func.rule = rule
        func.options = options
        return func
    return _deco