import click

from shipa.commands import constant


@click.group()
def cli_add():
    pass


@cli_add.command("add", short_help=constant.CMD_POOL_ADD)
@click.argument("pool", required=True)
@click.option('-d', '--default', is_flag=True, help=constant.OPT_POOL_DEFAULT)
@click.option('-p', '--public', is_flag=True, help=constant.OPT_POOL_PUBLIC)
@click.option('--accept-drivers', help=constant.OPT_POOL_DRIVER, multiple=True)
@click.option('--app-quota-limit', help=constant.OPT_POOL_QUOTA_LIMIT, type=int)
@click.option('--provisioner', help=constant.OPT_POOL_PROVISIONER)
@click.option('--plan', help=constant.OPT_POOL_PLAN)
@click.option('--kubernetes-namespace', help=constant.OPT_POOL_NAMESPACE)
@click.pass_obj
def create(env, pool, default, public, accept_drivers, app_quota_limit, provisioner, plan, kubernetes_namespace):
    """Each docker node added by shipa engine belongs to one pool."""

    with env.client.http as http_client:
        env.client.auth(http_client)
        env.client.pool_add(pool=pool, default=default, public=public, accept_drivers=accept_drivers,
                            app_quota_limit=app_quota_limit, provisioner=provisioner, plan=plan,
                            kubernetes_namespace=kubernetes_namespace)
        print('Pool successfully registered.')


@click.group()
def cli_remove():
    pass


@cli_remove.command("remove", short_help=constant.CMD_POOL_REMOVE)
@click.argument("pool", required=True)
@click.pass_obj
def remove(env, pool):
    """Remove an existing pool."""

    with env.client.http as http_client:
        env.client.auth(http_client)
        env.client.pool_remove(pool=pool)
        print('Pool successfully removed.')


@click.group()
def cli_update():
    pass


@cli_update.command("update", short_help=constant.CMD_POOL_UPDATE)
@click.argument("pool", required=True)
@click.option('-d', '--default', is_flag=True, help=constant.OPT_POOL_DEFAULT)
@click.option('-p', '--public', is_flag=True, help=constant.OPT_POOL_PUBLIC)
@click.option('--accept-drivers', help=constant.OPT_POOL_DRIVER, multiple=True)
@click.option('--app-quota-limit', help=constant.OPT_POOL_QUOTA_LIMIT, type=int)
@click.option('--plan', help=constant.OPT_POOL_PLAN)
@click.pass_obj
def update(env, pool, default, public, accept_drivers, app_quota_limit, plan):
    """Updates attributes for a pool."""

    with env.client.http as http_client:
        env.client.auth(http_client)
        env.client.pool_update(pool=pool, default=default, public=public, accept_drivers=accept_drivers,
                               app_quota_limit=app_quota_limit, plan=plan)
        print('Pool successfully updated.')


cli = click.CommandCollection(sources=[cli_add, cli_remove, cli_update])
