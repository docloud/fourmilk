# coding=utf8

from flask import make_response
from flask.views import MethodView

from webargs import fields
from webargs.flaskparser import use_args

from fourmilk.models import mongo
from fourmilk.decorators import router


class PartView(MethodView):
    route = '/part'

    def get(self):
        return {'a': 1}


class UserView(MethodView):
    route = '/user'

    login_args = {
        "username": fields.Str(require=True),
        "password": fields.Str(require=True)
    }
    register_args = login_args

    @use_args(login_args)
    @router('login', methods=('POST',))
    def login(self, args):
        user = mongo.part.find_one(args)
        if user:
            user.pop('_id')
            return user
        else:
            return dict(status=200, message=None)

    @use_args(register_args)
    def register(self, args):
        user_id = mongo.part.insert(args)
        return dict(data=str(user_id))


__all__ = [
    PartView,
    UserView
]
