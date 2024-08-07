import urllib.parse
import json
import requests
import threading
from flask import request, Response
from slack_specific.slack_request_verification import verify_slack_request
from slack_specific.slack_app_verification import verify_slack_app
from slack_specific.slack_user_verification import verify_slack_user
from command_handlers.sentinel import run_sentinel_command
from command_handlers.defender import run_defender_command
from command_handlers.elastic import run_elastic_command
from command_handlers.tenable import run_tenable_command
from command_handlers.common import run_common_command

def send_response(response_url, response_message):
    headers = {
        'Content-Type': 'application/json'
    }
    response_data = {
        "text": response_message
    }
    requests.post(response_url, json=response_data, headers=headers)

def handle_slack_command(text, response_url):
    if text.startswith("sentinel "):
        sentinel_text = text[len("sentinel "):].strip()
        response_message = run_sentinel_command(sentinel_text)
    elif text.startswith("defender "):
        defender_text = text[len("defender "):].strip()
        response_message = run_defender_command(defender_text)
    elif text.startswith("elastic "):
        elastic_text = text[len("elastic "):].strip()
        response_message = run_elastic_command(elastic_text)
    elif text.startswith("tenable "):
        tenable_text = text[len("tenable "):].strip()
        response_message = run_tenable_command(tenable_text)
    else:
        response_message = run_common_command(text)
    
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

    if not verify_slack_user(user_id):
        return Response("Access denied", status=200)

    threading.Thread(target=handle_slack_command, args=(text, response_url)).start()

    return Response(status=200)

