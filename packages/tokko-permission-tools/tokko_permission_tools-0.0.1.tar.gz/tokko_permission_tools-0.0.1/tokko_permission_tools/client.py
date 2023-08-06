from urllib.parse import urlencode
from dataclasses import dataclass
from typing import List
import logging
import json

from requests.exceptions import ConnectionError, HTTPError
import requests

log = logging.getLogger(__name__)


@dataclass(init=True)
class ErrorDataType:

    message: str
    exception: Exception = None
    status: int = None

    def __str__(self):

        exception = self.exception or Exception(self.message)
        status = self.status or "-"

        return f"{self.message} - " \
               f"{type(exception).__name__} " \
               f"[{status}]"


class Validator:

    __errors__: List[ErrorDataType] = []
    fail_safe: bool = True
    auto_init: bool = True

    def validate(self):

        validators = [m for m in dir(self) if m.startswith("validate_")]
        validators = [getattr(self, v) for v in validators if callable(getattr(self, v))]

        for validator in validators:
            try:
                validator()
            except Exception as e:
                if not self.fail_safe:
                    raise e
                self.add_errors(message=f"{validator.__name__}.{validator.__doc__}.{e}", exception=e)

        return len(self.errors) == 0

    def is_valid(self):
        try:
            if not self.validate():
                raise ValueError(", ".join([f"{err}" for err in self.errors]))

            return True

        except Exception as e:
            log.error(e)
            if not self.fail_safe:
                raise e

            return False

    @property
    def errors(self) -> list:
        return self.__errors__

    def add_errors(self, message, **extras):

        exception = extras.get("exception")
        status = extras.get("status")
        self.__errors__.append(ErrorDataType(exception=exception,
                                             message=message,
                                             status=status))

    def __post_init__(self):
        if self.auto_init:
            self.validate()


@dataclass(init=True)
class User(Validator):
    user: str = None
    permission: list = None

    def validate_user_id_not_empty(self):
        if not self.user:
            raise ValueError("USER_ID argument is required")

    def __render_permission__(self):
        ...

    def permissions(self) -> list:
        perms = []
        for permission in self.permission:
            if permission and isinstance(permission, str):
                namespace, action = permission.split(":")
                if all([namespace, action]):
                    perms.append(Permission(namespace=namespace, action=action))
        return perms

    def as_dict(self) -> dict:
        return {
            "user_id": self.user,
            "permissions": self.permission
        }

    def __str__(self) -> str:
        return json.dumps(self.as_dict(), indent=4)


@dataclass(init=True)
class Permission(Validator):

    namespace: str = ""
    action: str = ""
    description: str = ""
    permission: str = ""
    auto_test: bool = True

    def validate_namespace_not_empty(self):
        if not self.namespace:
            raise ValueError("NAMESPACE argument is required.")

        return True

    def validate_action_not_empty(self):
        if not self.action:
            raise ValueError("ACTION argument is required.")

        return True

    @property
    def claim(self) -> str:
        return f"{self.namespace}:{self.action}"

    def __post_init__(self):
        if self.auto_test:
            self.validate()

    def __str__(self) -> str:
        return self.claim


class API:

    session = None
    token = None
    headers = None

    def __init__(self, home_url, **options):
        headers = options.get("headers", {})
        self.token = options.get("token")
        self.home_url = home_url
        self.session = requests.Session()
        if self.token:
            headers.update({"Authorization": f"Bearer {self.token}"})
        headers.update({"Content-Type": "application/json"})
        self.headers = headers
        self.session.headers.update(self.headers)

    def run_query(self, url: str, method: str = None, **data):
        log.debug(f"Has Token: {self.token is not None}")
        log.debug(f"Headers: {json.dumps(self.headers, indent=4)}")
        method = method or "get"
        allowed_methods = ["post", "get", "put", "delete"]
        if method.lower() not in allowed_methods:
            raise ValueError("Unsupported method")

        try:
            if method.lower() == "get" and data:
                raise IOError("GET not supports DATA")
            _method_fn = getattr(self.session, method.lower())
            r = _method_fn(url, data=json.dumps(data))
            if not r.status_code == 200:
                r.raise_for_status()
            if "application/json" not in r.headers.get("Content-Type", ""):
                raise TypeError(f"ContentType Error [{self.__name__}]. Unsupported response ContentType")

            return r.json()

        except (ConnectionError, HTTPError) as conn_err:
            raise IOError(f"Connection Error [{type(self).__name__}] - {conn_err}") from conn_err


class PermissionManager(API):

    def add(self, namespace: str, action: str, description: str = None):
        try:
            res = self.run_query(url=f"{self.home_url}/permissions", method='post',
                                 # Data
                                 namespace=namespace,
                                 action=action,
                                 description=description or "")
            return Permission(**res)
        except Exception as add_error:
            raise IOError(f"Add permission fails. {add_error}") from add_error

    def delete(self, namespace: str, action: str):

        try:
            return self.run_query(url=f"{self.home_url}/permissions", method="delete",
                                  # Data
                                  namespace=namespace,
                                  action=action)
        except Exception as delete_error:
            raise IOError(f"Delete permission fails. {delete_error}") from delete_error

    def get(self, pid: str):

        url = f"{self.home_url}/permissions?{urlencode(dict(pid=pid))}/"
        res = self.run_query(url=url, method='get')
        if res:
            return Permission(**res[0])
        raise IOError("Not Found")

    def list(self, **filters):

        try:
            permissions_url = f"{self.home_url}/permissions"
            if filters:
                permissions_url = f"{permissions_url}?{urlencode(filters)}"
            res = self.run_query(url=permissions_url, method='get')
            if res:
                return [Permission(**permission) for permission in res]
            return []

        except Exception as list_error:
            raise IOError(f"List permission fails. {list_error}") from list_error


class UserPermissionManager(API):

    def grant(self, user_id, namespace, action):

        try:
            permissions_url = f"{self.home_url}/permissions/{user_id}/{namespace}:{action}"
            result = self.run_query(url=permissions_url, method='post')
            return result
        except Exception as grant_error:
            raise IOError(f"Grant Permission fails. {grant_error}") from grant_error

    def revoke(self, user_id, namespace, action):

        try:
            permissions_url = f"{self.home_url}/permissions/{user_id}/{namespace}:{action}"
            result = self.run_query(url=permissions_url, method='delete')
            return result
        except Exception as revoke_error:
            raise IOError(f"Revoke Permission fails. {revoke_error}") from revoke_error

    def get(self, user_id):

        try:
            permissions_url = f"{self.home_url}/permissions/{user_id}"
            print(f"Permissions URL: {permissions_url}")
            user_permissions = self.run_query(url=permissions_url, method='get')
            return User(**user_permissions)
        except Exception as info_error:
            raise IOError(f"User Info fetch fails. {info_error}") from info_error


class TokkoPermissionClient:

    def __init__(self, home_url, permissions_class=None, user_permission_class=None, **options):
        token, headers = (options.get("token"), options.get("headers", {}))
        permissions_class = permissions_class or PermissionManager
        user_permission_class = user_permission_class or UserPermissionManager
        self.permissions = permissions_class(
            home_url=home_url,
            headers=headers,
            token=token
        )
        self.users = user_permission_class(
            home_url=home_url,
            headers=headers,
            token=token
        )
