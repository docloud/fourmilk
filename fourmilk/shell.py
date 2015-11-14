# coding=utf8

import click
from fourmilk import init


@click.group()
def cli():
    pass


@click.command()
def serve():
    init.run_app()


cli.add_command(serve)
