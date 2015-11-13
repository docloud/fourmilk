# coding=utf8

from . import app, config
from .api import __all__
import inspect
from flask.views import MethodView


def init_app():
    exclude = [pair[0] for pair in inspect.getmembers(MethodView)]
    exclude.extend(['get', 'post', 'put', 'delete', 'options', 'head', 'route'])

    for api in __all__:
        ins = api()

        # 获取所有额外的方法
        methods = inspect.getmembers(api)
        for key, method in methods:
            if key.startswith('__') or key in exclude:
                continue

            # 将MethodView中额外的方法绑定到APP的路由上
            # 绑定规则是
            # MethodView的路由后接方法名
            app.add_url_rule(
                '/'.join([api.route, key]),
                view_func=getattr(ins, key)
            )
        app.add_url_rule(api.route, view_func=api.as_view(api.__class__.__name__))


def run_app():
    init_app()
    from pprint import pprint

    pprint(app.url_map)
    app.run(host=config.get('host') or '127.0.0.1', port=config.get('port') or 3000)


if __name__ == '__main__':
    run_app()
