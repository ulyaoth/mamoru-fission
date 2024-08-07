# command_handlers/sentinel.py

import re
from commands.sentinel.cve import run_cve_command
from error_handler.error import error_unknown_sentinel_command

def run_sentinel_command(command: str) -> str:
    if re.match(r'^cve-\d{4}-\d{4,7}$', command):  # CVE validation
        return run_cve_command(command)
    else:
        return error_unknown_sentinel_command(command)