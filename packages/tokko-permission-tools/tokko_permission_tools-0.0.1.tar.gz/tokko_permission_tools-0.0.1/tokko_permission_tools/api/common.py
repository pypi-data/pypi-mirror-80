from typing import Tuple
import os

from tokko_permission_tools import Client


def get_config() -> Tuple[str, str]:
    """
    Build Config helper
    ---
    Required ENV variables:
    export AUTH_PERMISSION_TOKEN={your-auth-token}
    export AUTH_PERMISSION_API_HOME={tokko-permission-api-home-url}
    """
    token = os.environ.get("AUTH_PERMISSION_TOKEN")
    api_home = os.environ.get("AUTH_PERMISSION_API_HOME")
    if not token:
        raise SystemExit(f"ConfigError: Authorization TOKEN=\"{token or ''}\" was not found.\n"
                         f"{get_config.__doc__}")
    if not api_home:
        raise SystemExit(f"ConfigError: API_HOME=\"{api_home or ''}\" was not found."
                         f"{get_config.__doc__}")
    return token, api_home


def get_client(api_home: str, headers: dict = None, token: str = None):
    return Client(home_url=api_home, headers=headers, token=token)
