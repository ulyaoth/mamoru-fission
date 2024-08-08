# azure_specific/azure_token_access.py

import requests
import logging

def read_secret_from_file(path):
    try:
        with open(path, 'r') as file:
            return file.read().strip()
    except Exception as e:
        logging.error(f"Error reading secret from file: {e}")
        return None

def get_azure_token(api_name):
    # Define paths to secret files
    client_id_path = "/secrets/default/mamoru-secrets/AZURE_CLIENT_ID"
    client_secret_path = "/secrets/default/mamoru-secrets/AZURE_CLIENT_SECRET"
    tenant_id_path = "/secrets/default/mamoru-secrets/AZURE_TENANT_ID"

    # Read secrets from files
    client_id = read_secret_from_file(client_id_path)
    client_secret = read_secret_from_file(client_secret_path)
    tenant_id = read_secret_from_file(tenant_id_path)

    if not client_id or not client_secret or not tenant_id:
        logging.error("One or more required secrets are missing.")
        return None

    # Define the token endpoint
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

    # Map API names to scopes
    api_scopes = {
        "graph": "https://graph.microsoft.com/.default",
        "atp": "https://api.securitycenter.microsoft.com/.default"
    }

    # Get the appropriate scope based on the input
    scope = api_scopes.get(api_name.lower())
    if not scope:
        logging.error(f"Invalid API name provided: {api_name}")
        return None

    # Prepare the payload
    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': scope
    }

    try:
        # Make the POST request to get the token
        response = requests.post(token_url, data=payload)
        
        # Check if the request was successful
        response.raise_for_status()
        token = response.json().get('access_token')
        logging.debug(f"Access Token: {token}")
        return token
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to obtain token: {e}")
        logging.error(f"Response content: {e.response.content}")
        return None
