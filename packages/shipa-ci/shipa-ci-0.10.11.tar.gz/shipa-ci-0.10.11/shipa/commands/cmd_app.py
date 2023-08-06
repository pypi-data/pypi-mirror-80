import click

from shipa.commands import constant
from shipa.utils import validate_map
from shipa.client.types import AppExistsError


@click.group()
def cli_create():
    pass


@cli_create.command("create", short_help=constant.CMD_APP_CREATE)
@click.argument("appname", required=True)
@click.argument("platform", required=False)
@click.option('-d', '--description', help=constant.OPT_APP_CREATE_DESCRIPTION)
@click.option('-f', '--dependency-file', help=constant.OPT_APP_CREATE_DEPENDENCY, multiple=True)
@click.option('-g', '--tag', help=constant.OPT_APP_CREATE_TAG, multiple=True)
@click.option('-p', '--plan', help=constant.OPT_APP_CREATE_PLAN)
@click.option('-r', '--router', help=constant.OPT_APP_CREATE_ROUTER)
@click.option('--router-opts', help=constant.OPT_APP_CREATE_ROUTER_opt, callback=validate_map, multiple=True)
@click.option('-t', '--team', help=constant.OPT_APP_CREATE_TEAM, required=True)
@click.option('-o', '--pool', help=constant.OPT_APP_CREATE_POOL)
@click.option('--ignore-if-exists', help=constant.OPT_APP_CREATE_IGNORE_IF_EXISTS, default=False)
@click.pass_obj
def create(env, appname, platform, description, dependency_file, tag, plan, router, router_opts, team, pool, ignore_if_exists):
    """Creates a new app using the given name and platform."""

    with env.client.http as http_client:
        env.client.auth(http_client)
        try:
            env.client.app_create(appname, team=team, pool=pool, platform=platform, description=description,
                                dependency_files=dependency_file, tags=tag, plan=plan, router=router,
                                router_opts=router_opts)
        except AppExistsError as e:
            print(e)
            if ignore_if_exists:
                pass 


@click.group()
def cli_remove():
    pass


@cli_remove.command("remove", short_help=constant.CMD_APP_REMOVE)
@click.argument("appname", required=True)
@click.pass_obj
def remove(env, appname):
    """If the app is bound to any service instance, all binds will be removed before the app gets deleted"""

    with env.client.http as http_client:
        env.client.auth(http_client)
        env.client.app_remove(appname=appname)
        env.client.autoscale_check()
        print('App {0} has been removed!'.format(appname))


@click.group()
def cli_deploy():
    pass


@cli_deploy.command("deploy", short_help=constant.CMD_APP_DEPLOY)
@click.option('-a', '--app', 'appname', help=constant.OPT_APP_DEPLOY_APP, required=True)
@click.option('-d', '--directory', help=constant.OPT_APP_DEPLOY_DIRECTORY, default='.')
@click.option('--steps', help=constant.OPT_APP_DEPLOY_STEPS, type=int, default=1, show_default=True)
@click.option('--step-interval', help=constant.OPT_APP_DEPLOY_STEP_INTERVAL, default='1s', show_default=True)
@click.option('--step-weight', help=constant.OPT_APP_DEPLOY_STEP_WEIGHT, type=int, default=100, show_default=True)
@click.pass_obj
def deploy(env, appname, directory, steps, step_interval, step_weight):
    """Deploys set of directories to shipa server."""

    with env.client.http as http_client:
        env.client.auth(http_client)
        env.client.app_deploy(appname=appname, directory=directory, steps=steps, step_interval=step_interval,
                              step_weight=step_weight)
        env.client.autoscale_check()
        print('App {0} has been deployed!'.format(appname))


@click.group()
def cli_move():
    pass


@cli_remove.command("move", short_help=constant.CMD_APP_REMOVE)
@click.option('-a', '--app', 'appname', help=constant.OPT_APP_REMOVE_APP, required=True)
@click.option('-p', '--pool', help=constant.OPT_APP_CREATE_POOL, required=True)
@click.pass_obj
def move(env, appname, pool):
    """ Moves app to another pool """

    with env.client.http as http_client:
        env.client.auth(http_client)
        env.client.app_move(appname=appname, pool=pool)
        env.client.autoscale_check()
        print('App {0} has been moved!'.format(appname))


cli = click.CommandCollection(sources=[cli_create, cli_remove, cli_deploy, cli_move])
