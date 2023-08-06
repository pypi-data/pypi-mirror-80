#!/usr/bin/env python

import os
import sys
import click

from shipa.client.client import ShipaClient
from shipa.client.http import HttpClient

CONTEXT_SETTINGS = dict(auto_envvar_prefix="SHIPA")
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "commands"))


class Environment:
    def __init__(self, verbose=False, client=None, token=None):
        self.verbose = verbose
        self.client = client
        self.token = token

    def log(self, msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)

    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)


class ShipaCLI(click.MultiCommand):
    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith(".py") and filename.startswith("cmd_"):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            mod = __import__('shipa.commands.cmd_{}'.format(name), None, None, ["cli"])
        except ImportError as e:
            return
        return mod.cli


@click.command(cls=ShipaCLI, context_settings=CONTEXT_SETTINGS)
@click.option('-s', '--server', help='shipa server, for example http://shipa.org:8080', required=True)
@click.option('-e', '--email', help='user email')
@click.option('-p', '--password', help='user password')
@click.option('-t', '--token', help='token')
@click.option('--ca-cert', help='shipa ca certificate file')
@click.option('--ca', help='shipa ca certificate')
@click.option('--insecure', is_flag=True, help="enables ssl insecure mode")
@click.option('-v', '--verbose', is_flag=True, help="enables verbose mode")
@click.pass_context
def cli(ctx, server, email, password, token, ca_cert, ca, insecure, verbose):
    """A shipa command line interface."""

    client = ShipaClient(server=server, client=HttpClient(ca_cert=ca_cert, ca=ca, insecure=insecure), email=email,
                         password=password, verbose=verbose, token=token)
    ctx.obj = Environment(verbose=verbose, client=client)
