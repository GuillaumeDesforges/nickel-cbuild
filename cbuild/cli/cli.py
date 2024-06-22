import sys
import importlib
import click


def echo(msg: str):
    print(msg, file=sys.stderr)


@click.group()
def cli():
    pass


importlib.import_module("cbuild.cli.init")
importlib.import_module("cbuild.cli.build")
