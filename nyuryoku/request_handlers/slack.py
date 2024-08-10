import urllib.parse
import json
import requests
import threading
import role_handlers.roles # so the roles are loaded
from flask import request, Response
from slack_specific.slack_request_verification import verify_slack_request
from slack_specific.slack_app_verification import verify_slack_app
from command_handlers.command_registry import command_registry
from auth_handlers.auth_methods import verify_user

def send_response(response_url, response_message):
    headers = {
        'Content-Type': 'application/json'
    }

    # Check if response_message is a string or a list (blocks)
    if isinstance(response_message, str):
        response_data = {
            "text": response_message
        }
    elif isinstance(response_message, list):
        response_data = {
            "blocks": response_message
        }
    else:
        raise ValueError("response_message must be either a string (for text) or a list (for blocks).")

    response = requests.post(response_url, json=response_data, headers=headers)
    response.raise_for_status()

def handle_slack_command(text, response_url, myaccess, user_realname):
    # Split the command into its main prefix and the rest of the command
    command_parts = text.split(" ", 1)
    prefix = command_parts[0]
    command_body = command_parts[1] if len(command_parts) > 1 else ""

    # Check if the prefix exists in the registry
    if prefix in command_registry:
        # Call the associated handler function
        if prefix == "user":
            # If the command requires the real name, pass it as well
            response_message = command_registry[prefix](command_body, myaccess, user_realname)
        else:
            response_message = command_registry[prefix](command_body, myaccess)
    else:
        # Handle unknown commands or fall back to a default handler
        response_message = command_registry.get("common")(text, myaccess)

    send_response(response_url, response_message)

def handle_slack_request(req):
    request_body = req.data.decode('utf-8')

    try:
       if req.headers.get('Content-Type') == 'application/json':
            payload = json.loads(request_body)
       else:
            payload = {key: value for key, value in request.form.items()}
            request_body = urllib.parse.urlencode(payload)
    except Exception as e:
        return Response("Invalid request payload", status=400)  

    if not verify_slack_request(req, request_body):
        return Response(status=200)  # Return 200 without a body to silently discard the request

    user_id = payload.get('user_id')
    text = payload.get('text', '').lower().strip()
    api_app_id = payload.get('api_app_id')
    response_url = payload.get('response_url')

    if not verify_slack_app(api_app_id):
        return Response(status=200)  # Return 200 without a body to silently discard the request

    is_verified, myaccess, user_realname = verify_user(user_id)
    
    if not is_verified:
        return Response("Access denied", status=200)

    threading.Thread(target=handle_slack_command, args=(text, response_url, myaccess, user_realname)).start()

    return Response(status=200)

