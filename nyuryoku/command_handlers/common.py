# command_handlers/common.py

import re
from commands.common.help import get_slack_help_menu
from commands.common.cve import run_cve_command
from error_handler.error import error_slack_unknown_command

def run_common_command(command: str) -> str:
    if command == "help":
        return get_slack_help_menu()
    elif re.match(r'^cve-\d{4}-\d{4,7}$', command):
        return run_cve_command(command)
    else:
        return error_slack_unknown_command(command)