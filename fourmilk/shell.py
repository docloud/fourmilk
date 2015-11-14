# coding=utf8

import click
from fourmilk import init


@click.group()
def cli():
    pass


@click.command()
def serve():
    """
    启动服务
    """
    init.run_app()


@click.command('shell')
def start_ipython():
    """
    IPython 调试环境, 加载了预定义的对象和函数
    """
    from fourmilk import app, config, logger
    from fourmilk.decorators import decorator
    from fourmilk.models import mongo
    from fourmilk.exceptions import Error

    try:
        from tests import http
    except:
        pass

    import IPython

    IPython.embed()


cli.add_command(serve)
cli.add_command(start_ipython)