from tokko_permission_tools.api.common import get_config, get_client
from tokko_permission_tools.utils import render
from tokko_permission_tools.templates import (
    PERMISSION_DELETE_TEMPLATE as PERMISSION_DELETE,
    PERMISSION_LIST_TEMPLATE as PERMISSION_LIST,
    PERMISSION_NEW_TEMPLATE as PERMISSION_NEW,
    CLI_ERROR_TEMPLATE as CLI_ERROR,
)


def ls(quiet):
    """List Permissions"""
    try:
        token, api_home = get_config()
        client = get_client(api_home=api_home, headers={}, token=token)
        res = client.permissions.list()
        print(render(PERMISSION_LIST, **{"permissions": res, "be_verbose": not quiet}))
    except Exception as cli_error:
        raise SystemExit(render(CLI_ERROR, **dict(error=cli_error,
                                                  error_type=type(cli_error).__name__,
                                                  method="permission.list",
                                                  description="List permissions"))) from cli_error


def create(namespace: str, action: str, description: str = None):
    """Add new Permission"""
    try:
        token, api_home = get_config()
        client = get_client(api_home=api_home, headers={}, token=token)
        new_permission = client.permissions.add(namespace, action, description or "")
        print(render(PERMISSION_NEW, **{"permission": new_permission}))
    except Exception as cli_error:
        raise SystemExit(render(CLI_ERROR, **dict(error=cli_error,
                                                  error_type=type(cli_error).__name__,
                                                  method="permission.create",
                                                  description="Add new Permission"))) from cli_error


def delete(namespace: str, action: str):
    """Delete Permissions by namespace and action"""
    try:
        token, api_home = get_config()
        client = get_client(api_home=api_home, headers={}, token=token)
        res = client.permissions.delete(namespace, action)
        print(render(PERMISSION_DELETE, **{"action": res}))
    except Exception as cli_error:
        raise SystemExit(render(CLI_ERROR, **dict(error=cli_error,
                                                  error_type=type(cli_error).__name__,
                                                  method="permission.delete",
                                                  description="Delete Permission"))) from cli_error
