# role_handlers/roles.pu

import json
import logging

from role_handlers.role_registry import register_role

def read_config(key):
    config_path = f"/configs/default/mamoru-roles-configmap/{key}"
    try:
        with open(config_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        raise ValueError(f"Config key {key} not found in ConfigMap")

def load_roles_from_configmap():
    roles_data = read_config('roles')
    try:
        roles = json.loads(roles_data)
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse roles from ConfigMap: {e}")
        raise ValueError("Invalid roles format in ConfigMap")

    for role_name, permissions in roles.items():
        register_role(role_name, permissions)

# Load roles at application startup
load_roles_from_configmap()