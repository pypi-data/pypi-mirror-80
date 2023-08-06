USER_INFO_TEMPLATE = """UserInfo:
 User "{{ user_info.user }}" has:{% for permission in user_info.permission %}
 + {{ permission }}{% endfor %}
---
"""

USER_GRANT_PERMISSION_TEMPLATE = """{% if success %}OK{% else %}FUCK{% endif %}
"""

USER_REVOKE_PERMISSION_TEMPLATE = """{% if success %}OK{% else %}FUCK{% endif %}
"""

PERMISSION_LIST_TEMPLATE = """{% if permissions %}{% if not be_verbose %}{% for permission in permissions %}{{ permission }}
{% endfor %}{% else %}Permissions ({{ permissions|length }}):{% for permission in permissions %}
 {{ permission.description }}
 + Action: {{ permission.action }}
 + Namespace: {{ permission.namespace }}
 + Permission: {{ permission }}
 ---{% endfor %}{% endif %}{% else %}Nothing to show {{ permissions }}{% endif %}
"""

PERMISSION_DELETE_TEMPLATE = """{% if action.success %}OK{% else %}FUCK{% endif %}
"""

PERMISSION_NEW_TEMPLATE = """Action: {{ permission.action }}
Namespace: {{ permission.namespace }}
Description: {{ permission.description }}
"""


CLI_ERROR_TEMPLATE = """CLI ERROR - {{ method }} - Exception Raised {{ error_type }}.
Action {{ action }} fails. Message: {{ error }}
"""
