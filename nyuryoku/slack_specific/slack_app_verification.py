# slack_handler/slack_app_verification.py

import logging

def read_secret_from_file(path):
    try:
        with open(path, 'r') as file:
            return file.read().strip()
    except Exception as e:
        logging.error(f"Error reading secret from file: {e}")
        return None

def verify_slack_app(api_app_id: str) -> bool:
    expected_slack_app_id_path = "/secrets/default/mamoru-secrets/SLACK_APP_ID"
    expected_slack_app_id = read_secret_from_file(expected_slack_app_id_path)

    if not expected_slack_app_id:
        logging.error("Failed to retrieve SLACK_APP_ID from file.")
        return False

    # Check if the api_app_id matches the expected slack_app_id
    if api_app_id != expected_slack_app_id:
        logging.warning(f"Request from unauthorized app: {api_app_id}")
        return False

    return True
