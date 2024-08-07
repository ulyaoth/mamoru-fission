import hashlib
import hmac
import time
import logging

def read_secret_from_file(path):
    try:
        with open(path, 'r') as file:
            return file.read().strip()
    except Exception as e:
        logging.error(f"Error reading secret from file: {e}")
        return None

def verify_slack_request(req, request_body) -> bool:
    slack_signing_secret_path = "/secrets/default/mamoru-secrets/SLACK_SIGNING_SECRET"
    slack_signing_secret = read_secret_from_file(slack_signing_secret_path)

    if not slack_signing_secret:
        logging.error("Slack signing secret is not set in environment variables.")
        return False

    # Extract headers
    timestamp = req.headers.get('X-Slack-Request-Timestamp')
    slack_signature = req.headers.get('X-Slack-Signature')

    logging.info(f"Timestamp: {timestamp}")
    logging.info(f"Slack Signature: {slack_signature}")

    if not timestamp or not slack_signature:
        logging.error("Missing timestamp or signature.")
        return False

    # Check for replay attacks (timestamp should not be older than 5 minutes)
    if abs(time.time() - int(timestamp)) > 60 * 5:
        logging.error("Request timestamp is too old.")
        return False

    # Create the basestring as described by Slack
    sig_basestring = f'v0:{timestamp}:{request_body}'

    logging.info(f"Sig Basestring: {sig_basestring}")

    # Create the HMAC SHA256 signature
    my_signature = 'v0=' + hmac.new(
        slack_signing_secret.encode('utf-8'),
        sig_basestring.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    logging.info(f"My Signature: {my_signature}")

    # Compare the signatures
    if hmac.compare_digest(my_signature, slack_signature):
        logging.info("Signature verification successful.")
        return True
    else:
        logging.error("Signature verification failed.")
        return False
