# coding=utf8

from flask import make_response, jsonify
from flask.views import MethodView

from webargs import fields
from bson.objectid import ObjectId

from fourmilk.models import mongo
from fourmilk.decorators import router, use_args, use_kwargs, flask_useargs
from fourmilk.exceptions import Error


class PartView(MethodView):
    route = '/part'

    def get(self):
        parts = list(mongo.part.find())
        for part in parts:
            part['_id'] = str(part['_id'])
        return parts

    post_args = {
        "name": fields.Str(required=True),
        "amount": fields.Int(missing=0),
        "limit": fields.Int(missing=10),
        "order": fields.Int(missing=0),
        "master": fields.Str(required=True),
        "second": fields.Str(missing=""),
        "price": fields.Float(required=True)
    }

    @use_args(post_args)
    def post(self, args):
        return str(mongo.part.insert(args))

    def __ckeck_existed(self, id):
        object_id = ObjectId(id)
        part = mongo.part.find_one({'_id': object_id})
        if not part:
            raise Error(Error.PART_NOT_EXIST)
        return part

    order_args = {
        "id": fields.Str(required=True),
        "value": fields.Integer(required=True)
    }

    @use_args(order_args)
    @router('order', methods=('PUT',))
    def order(self, args):
        part = self.__ckeck_existed(args['id'])
        return mongo.part.update(
            {'_id': part['_id']},
            {'$set': {'order': part['order'] + args['value']}}
        )

    in_args = order_args

    @use_args(in_args)
    @router('in', methods=('PUT',))
    def part_in(self, args):
        part = self.__ckeck_existed(args['id'])
        if part['order'] < args['value']:
            raise Error(Error.PART_AMOUNT_ERROR)
        return mongo.part.update(
            {'_id': part['_id']},
            {'$set': {
                'order': part['order'] - args['value'],
                'amount': part['amount'] + args['value']
            }}
        )

    out_args = order_args

    @use_args(out_args)
    @router('out', methods=('PUT',))
    def part_out(self, args):
        part = self.__ckeck_existed(args['id'])
        if part['amount'] < args['value']:
            raise Error(Error.PART_AMOUNT_ERROR)
        return mongo.part.update(
            {'_id': part['_id']},
            {'$set': {'amount': part['amount'] - args['value']}}
        )


class UserView(MethodView):
    route = '/user'

    login_args = {
        "username": fields.Str(required=True),
        "password": fields.Str(required=True)
    }
    register_args = login_args.copy()
    register_args.update(role=fields.Int(missing=2))

    def _login(self, args):
        user = mongo.user.find_one(args)
        if user:
            user['id'] = str(user.pop('_id'))
            resp = make_response(jsonify(user))
            for k, v in user.iteritems():
                resp.set_cookie(k, str(v))
            return resp
        else:
            raise Error(Error.USER_NOT_EXIST)

    @use_args(login_args)
    @router('login', methods=('POST',))
    def login(self, args):
        return self._login(args)

    @use_args(register_args)
    @router('register', methods=('POST',))
    def register(self, args):
        self.exist(username=args["username"])
        mongo.user.insert(args)
        return self._login(args)

    exist_args = {
        "username": fields.Str(required=True)
    }

    @use_kwargs(exist_args)
    @router('exist')
    def exist(self, username):
        if mongo.user.find_one({"username": username}):
            raise Error(Error.USER_EXISTED)


__all__ = [
    PartView,
    UserView
]
