from tokko_permission_tools.api.common import get_client, get_config
from tokko_permission_tools.templates import (
    USER_REVOKE_PERMISSION_TEMPLATE as REVOKE_PERMISSION,
    USER_INFO_TEMPLATE as USER_INFO,
    CLI_ERROR_TEMPLATE as CLI_ERROR,
)
from tokko_permission_tools.utils import render


def info(user):
    """Get user permission info"""
    try:
        token, api_home = get_config()
        client = get_client(api_home=api_home, headers={}, token=token)
        res = client.users.get(user)
        print(render(USER_INFO, **{"user_info": res}))
    except Exception as cli_error:
        raise SystemExit(render(CLI_ERROR, **dict(action=cli_error,
                                                  error_type=type(cli_error).__name__,
                                                  description="Retrieve user permission info",
                                                  method="permission.user.info"))) from cli_error


def grant(user, namespace: str, action: str):
    """Grant user permission"""
    try:
        token, api_home = get_config()
        client = get_client(api_home=api_home, headers={}, token=token)
        res = client.users.grant(user, namespace, action)
        print(render(USER_INFO, **{"user_info": res}))
    except Exception as cli_error:
        raise SystemExit(render(CLI_ERROR, **dict(error=cli_error,
                                                  method="user.permission.grant",
                                                  error_type=type(cli_error).__name__,
                                                  description="Grant user permission"))) from cli_error


def revoke(user, namespace: str, action: str):
    """Revoke user permission"""
    try:
        token, api_home = get_config()
        client = get_client(api_home=api_home, headers={}, token=token)
        res = client.users.grant(user, namespace, action)
        print(render(REVOKE_PERMISSION, user=user, namespace=namespace, **res))
    except Exception as cli_error:
        raise SystemExit(render(CLI_ERROR, **dict(error=cli_error,
                                                  method="user.permission.revoke",
                                                  error_type=type(cli_error).__name__,
                                                  description="Revoke user permission"))) from cli_error
