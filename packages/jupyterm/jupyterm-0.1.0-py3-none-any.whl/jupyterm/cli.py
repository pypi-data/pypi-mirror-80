# -*- coding: utf-8 -*-

from pprint import pprint

import click

from .utils import find_project, licenses, classifiers


@click.group("jupyterm")
@click.pass_context
def cli(*args, **kwargs):
    """Jupyter + terminal = ♥."""
    pass
