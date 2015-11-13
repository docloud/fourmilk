# coding=utf8

from flask.views import MethodView
from flask import jsonify
from fourmilk import app, config, logger
from fourmilk.models import mongo


class PartView(MethodView):
    route = '/part'

    def get(self):
        return jsonify(a=1)

    def hello(self):
        return jsonify(mongo.part.find())


__all__ = [
    PartView,
]