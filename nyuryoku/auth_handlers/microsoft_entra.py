# auth_handlers/microsoft_entra.py

import asyncio
import json
import requests
from azure_specific.azure_graph_access import get_azure_graph_access, close_azure_graph_access

# Function to read configuration from the ConfigMap
def read_config(key):
    config_path = f"/configs/default/mamoru-configmap/{key}"
    try:
        with open(config_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        raise ValueError(f"Config key {key} not found in ConfigMap")

# Function to read sensitive information from Secrets
def read_secret(key):
    secret_path = f"/secrets/default/mamoru-secrets/{key}"
    try:
        with open(secret_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        raise ValueError(f"Secret key {key} not found in Secrets")

# Function to parse group configuration from JSON
def parse_group_config():
    group_data = read_config('MICROSOFT_ENTRA_GROUPS')
    try:
        groups = json.loads(group_data)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error parsing group configuration: {e}")
    return groups

# Load group configuration
GROUPS = parse_group_config()

# Function to get user information from Slack
def get_user_email_from_slack(slack_user_id):
    slack_token = read_secret('SLACK_BOT_OAUTH_TOKEN')  # Use the secret path for the token
    url = 'https://slack.com/api/users.info'
    headers = {
        'Authorization': f'Bearer {slack_token}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    params = {
        'user': slack_user_id
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        user_info = response.json()
        if user_info['ok']:
            return user_info['user']['profile']['email']
        else:
            raise Exception(f"Slack API error: {user_info['error']}")
    else:
        raise Exception(f"Failed to retrieve user info from Slack: {response.status_code}")

# Async function to get the user's ID from Azure AD, handling the potential external user format
async def get_user_id(graph_client, email):
    users = await graph_client.users.get()
    user = next((user for user in users.value if user.user_principal_name == email), None)

    if not user:
        tenant_name = await get_tenant_name(graph_client)
        alternative_email = email.replace('@', '_') + '#EXT#@' + tenant_name
        user = next((user for user in users.value if user.user_principal_name == alternative_email), None)

    if user:
        return user.id
    else:
        raise Exception(f"No user found with email {email} or its external format")

# Async function to get the tenant name
async def get_tenant_name(graph_client):
    organization = await graph_client.organization.get()
    return organization.value[0].verified_domains[0].name

# Async function to get the user's group memberships
async def get_user_groups_from_azure_ad_async(graph_client, user_id):
    memberships = await graph_client.users.by_user_id(user_id).transitive_member_of.get()
    group_ids = [group.id for group in memberships.value if group.odata_type == '#microsoft.graph.group']
    return group_ids

# Main function to verify the user (Async)
async def verify_microsoft_entra_user_async(slack_user_id, source):
    # Step 1: Get the user's email from Slack
    if source == "slack":
        email = get_user_email_from_slack(slack_user_id)
    else:
        raise ValueError("Unsupported source for Microsoft Entra verification")

    # Step 2: Get Azure AD Graph client and credentials
    graph_client, credential = await get_azure_graph_access()

    try:
        # Step 3: Get the user's ID from Azure AD
        user_id = await get_user_id(graph_client, email)

        # Step 4: Get the user's group memberships from Azure AD
        user_groups = await get_user_groups_from_azure_ad_async(graph_client, user_id)

        # Step 5: Determine the user's role based on group membership
        for role, group_info in GROUPS.items():
            if group_info['id'] in user_groups:
                return True, role, email

        # If the user is not in any of the defined groups, deny access
        return False, None, None

    except Exception as e:
        raise Exception(f"Verification failed: {e}")
    finally:
        # Ensure to close the credential properly
        await close_azure_graph_access(credential)

# Wrapper to use in sync code
def verify_microsoft_entra_user(slack_user_id, source):
    return asyncio.run(verify_microsoft_entra_user_async(slack_user_id, source))
