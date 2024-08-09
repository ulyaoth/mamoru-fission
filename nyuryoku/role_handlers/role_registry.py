# role_registry.py

role_permissions_registry = {}

def register_role(role_name: str, permissions: list):
    """Register a role with its associated permissions."""
    if role_name in role_permissions_registry:
        role_permissions_registry[role_name].extend(permissions)
    else:
        role_permissions_registry[role_name] = permissions

def check_permission(permission: str, user_role: str) -> bool:
    """Check if a user role has permission to execute a command."""
    if user_role == "admin":
        return True  # Admins have access to everything
    return permission in role_permissions_registry.get(user_role, [])
