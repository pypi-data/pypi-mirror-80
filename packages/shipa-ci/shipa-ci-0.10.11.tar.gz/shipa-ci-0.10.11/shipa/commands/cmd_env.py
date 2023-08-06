import click

from shipa.commands import constant
from shipa.utils import validate_env


@click.group()
def cli_set():
    pass


@cli_set.command("set", short_help=constant.CMD_ENV_SET)
@click.argument('env-variables', nargs=-1, required=True, callback=validate_env)
@click.option('-a', '--app', 'app_name', help=constant.OPT_ENV_APP, required=True)
@click.option('-p', '--private', is_flag=True, help=constant.OPT_ENV_PRIVATE)
@click.option('--no-restart', is_flag=True, help=constant.OPT_ENV_NO_RESTART)
@click.pass_obj
def set(env, env_variables, app_name, private, no_restart):
    """Set environment variables"""

    with env.client.http as http_client:
        env.client.auth(http_client)
        env.client.env_set(app_name=app_name, envs=env_variables, private=private, no_restart=no_restart)
        print('Environment variables successfully is successfully set.')


@click.group()
def cli_unset():
    pass


@cli_unset.command("unset", short_help=constant.CMD_ENV_UNSET)
@click.argument('env-variables', nargs=-1, required=True)
@click.option('-a', '--app', 'app_name', help=constant.OPT_ENV_APP, required=True)
@click.option('--no-restart', is_flag=True, help=constant.OPT_ENV_NO_RESTART)
@click.pass_obj
def unset(env, env_variables, app_name, no_restart):
    """Remove environment variables"""

    with env.client.http as http_client:
        env.client.auth(http_client)
        env.client.env_unset(app_name=app_name, envs=env_variables, no_restart=no_restart)
        print('Environment variables successfully removed.')


cli = click.CommandCollection(sources=[cli_set, cli_unset])
