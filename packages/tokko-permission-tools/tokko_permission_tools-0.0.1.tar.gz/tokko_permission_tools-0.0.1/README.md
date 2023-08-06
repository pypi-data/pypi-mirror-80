Auth Permission Tools
---

### Before start

#### TokkoPermissionTools Credentials:
```bash
export AUTH_PERMISSION_TOKEN={your-tokko-auth-token}
export AUTH_PERMISSION_API_HOME={tokko-permission-api-home-url}
```

### Users

#### Retrieve user permissions
```python

from tokko_permission_tools.api.users import info
user = "t.stark@navent.com"
# Get user permissions info
info(user)
```

**Response**:
```
UserInfo:
 User "t.stark@navent.com" has:
 + markII_suite:activate
 + markI_suite:weapon_test
 + markI_suite:auto_test
   ...
 + markII_suite:remove_ark_reactor
---

```
