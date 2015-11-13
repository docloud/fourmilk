# coding=utf8

from flask.views import MethodView
from flask import jsonify
from fourmilk.models import mongo

from webargs import fields
from webargs.flaskparser import use_args

login_args = {
    "username": fields.Str(require=True),
    "password": fields.Str(require=True)
}


class PartView(MethodView):
    route = '/part'

    @use_args(login_args)
    def login(self, args):
        user = mongo.part.find_one(args)
        user.pop('_id')
        if user:
            return jsonify(user), 200
        else:
            return jsonify(status=200, message=None), 401

    @use_args(login_args)
    def register(self, args):
        status = mongo.part.insert(args)
        return jsonify(data=str(status))


__all__ = [
    PartView,
]
