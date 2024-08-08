# command_handlers/defender.py

from commands.defender.help import get_defender_help_menu
from commands.defender.cve import run_cve_command
from commands.defender.vulnerabilities import run_vulnerabilities_command
from error_handler.errors import error_unknown_command


def run_defender_command(command: str) -> str:
    if command == "help":
        return get_defender_help_menu()
    elif command.startswith("check-cve "):
        cve_input = command[len("check-cve "):].strip()
        return run_cve_command(cve_input)
    elif command.startswith("vulnerabilities "):
        vulnerabilities_input = command[len("vulnerabilities "):].strip()
        return run_vulnerabilities_command(vulnerabilities_input)
    else:
        return error_unknown_command(command, "defender")