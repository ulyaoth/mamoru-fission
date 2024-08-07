# azure_specific/azure_graph_access.py

import logging
from azure.identity.aio import ClientSecretCredential
from msgraph import GraphServiceClient

def read_secret_from_file(path):
    try:
        with open(path, 'r') as file:
            return file.read().strip()
    except Exception as e:
        logging.error(f"Error reading secret from file: {e}")
        return None

# Value for the scope
scopes = ['https://graph.microsoft.com/.default']

# Values from the app registration
client_id_path = "/secrets/default/mamoru-secrets/AZURE_CLIENT_ID"
client_secret_path = "/secrets/default/mamoru-secrets/AZURE_CLIENT_SECRET"
tenant_id_path = "/secrets/default/mamoru-secrets/AZURE_TENANT_ID"

# Read secrets from files
client_id = read_secret_from_file(client_id_path)
client_secret = read_secret_from_file(client_secret_path)
tenant_id = read_secret_from_file(tenant_id_path)

async def get_azure_graph_access():
    credential = ClientSecretCredential(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret)

    await credential.__aenter__()  # Properly initialize the async credential

    graph_client = GraphServiceClient(credential, scopes)

    return graph_client, credential

async def close_azure_graph_access(credential):
    await credential.__aexit__(None, None, None)