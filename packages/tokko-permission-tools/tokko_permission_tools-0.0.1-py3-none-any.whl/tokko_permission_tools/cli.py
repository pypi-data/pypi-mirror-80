import click

from tokko_permission_tools.api.users import (
    info as user_permission_info,
    revoke as revoke_user_permission,
    grant as grant_user_permission
)
from tokko_permission_tools.api.permission import (
    ls as list_permission,
    delete as delete_permission,
    create as create_permission,
)


@click.group()
def main():
    """Tokko Permission CLI"""


@main.group()
def users():
    """User permission tools"""


@users.command()
@click.argument("user", type=str)
def info(user):
    """Get user permission info"""
    user_permission_info(user)


@users.command()
@click.argument("user", type=str)
@click.argument("namespace", type=str)
@click.argument("action", type=str)
def grant(user, namespace: str, action: str):
    """Grant user permission"""
    grant_user_permission(user, namespace, action)


@users.command()
@click.argument("user", type=str)
@click.argument("namespace", type=str)
@click.argument("action", type=str)
def revoke(user, namespace: str, action: str):
    """Revoke user permission"""
    revoke_user_permission(user, namespace, action)


@main.group()
def permissions():
    """Permission tools"""


@permissions.command()
@click.option("-q", "--quiet", is_flag=True)
def ls(quiet):
    """List Permissions"""
    list_permission(quiet)


@permissions.command()
@click.option("-q", "--quiet", is_flag=True)
def ls(quiet):
    """List Permissions"""
    list_permission(quiet)


@permissions.command()
@click.argument("namespace", type=str)
@click.argument("action", type=str)
@click.argument("description", type=str, default="")
def create(namespace: str, action: str, description: str = None):
    """Revoke user permission"""
    create_permission(namespace, action, description or "")


@permissions.command()
@click.argument("namespace", type=str)
@click.argument("action", type=str)
def delete(namespace: str, action: str):
    """Revoke user permission"""
    delete_permission(namespace, action)
