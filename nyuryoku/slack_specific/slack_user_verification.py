# slack_specific/slack_user_verification.py

import json
import logging

def read_config_from_file(path):
    try:
        with open(path, 'r') as file:
            return file.read().strip()
    except Exception as e:
        logging.error(f"Error reading config from file: {e}")
        return None

def get_authorized_users():
    authorized_users_path = "/configs/default/mamoru-configmap/AUTHORIZED_SLACK_USERS"
    authorized_users_str = read_config_from_file(authorized_users_path)

    if not authorized_users_str:
        logging.error("Failed to retrieve AUTHORIZED_SLACK_USERS from file")
        return []

    try:
        authorized_users = json.loads(authorized_users_str)
    except json.JSONDecodeError:
        logging.error("Failed to decode AUTHORIZED_SLACK_USERS from file")
        authorized_users = []
    return authorized_users

def verify_slack_user(user_id: str) -> bool:
    authorized_users = get_authorized_users()
    for user in authorized_users:
        if user["userid"] == user_id:
            return True
    logging.warning(f"Unauthorized user: {user_id}")
    return False
