# command_handlers/defender.py

import re
from commands.defender.help import get_defender_help_menu
from commands.defender.cve import run_cve_command
from error_handler.error import error_unknown_defender_command


def run_defender_command(command: str) -> str:
    if re.match(r'^cve-\d{4}-\d{4,7}$', command):  # CVE validation
        return run_cve_command(command)
    elif command == "help":
        return get_defender_help_menu()
    else:
        return error_unknown_defender_command(command)