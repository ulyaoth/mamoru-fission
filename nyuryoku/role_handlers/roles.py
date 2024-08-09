# role_handlers/roles.py

from role_handlers.role_registry import register_role

# Register the roles and their permissions, namespacing by command group
register_role('user', [
    'common:help',
    'common:version',
    'user:help',
    'user:myinfo'
])


# Additional roles can be added as needed
register_role('guest', ['common:help'])
