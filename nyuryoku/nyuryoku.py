# nyuryoku.py main function

from flask import Flask, request, Response
from request_handlers.slack import handle_slack_request
from request_handlers.teams import handle_teams_request

app = Flask(__name__)

def is_slack_request(req) -> bool:
    return 'x-slack-signature' in req.headers

def is_teams_request(req) -> bool:
    return 'X-Teams-Signature' in req.headers

@app.route('/nyuryoku', methods=['POST'])
def nyuryoku():
    if is_slack_request(request):
        return handle_slack_request(request)
    elif is_teams_request(request):
        return handle_teams_request(request)
    else:
        return Response("Invalid request source", status=400)
