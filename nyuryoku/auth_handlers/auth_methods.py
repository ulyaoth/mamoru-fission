# auth_handlers/auth_methods.py

from slack_specific.slack_user_verification import verify_slack_user

# Function to read the ConfigMap values
def read_config(key):
    config_path = f"/configs/default/mamoru-configmap/{key}"
    try:
        with open(config_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        raise ValueError(f"Config key {key} not found in ConfigMap")

# Load configuration from ConfigMap
auth_method = read_config('AUTH_METHOD')

def verify_microsoft_entra(user_id):
    return True

def verify_user(user_id):

    if auth_method == 'slack_user_verification':
        return verify_slack_user(user_id)
    elif auth_method == 'microsoft_entra':
        return verify_microsoft_entra(user_id)
    else:
        raise ValueError("Invalid authentication method")