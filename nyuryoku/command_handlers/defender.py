# command_handlers/defender.py

from commands.defender.help import get_defender_help_menu
from commands.defender.cve import run_cve_command
from commands.defender.vulnerabilities import run_vulnerabilities_command
from commands.defender.endpoint import run_endpoint_command
from role_handlers.role_registry import check_permission
from error_handler.errors import error_unknown_command, error_permission_denied


def run_defender_command(command: str, myaccess: str) -> str:
    # Use namespaced permission checks
    if command == "help":
        if check_permission("defender:help", myaccess):
            return get_defender_help_menu()
        else:
            return error_permission_denied(command)
    
    elif command.startswith("check-cve "):
        if check_permission("defender:check-cve", myaccess):
            cve_input = command[len("check-cve "):].strip()
            return run_cve_command(cve_input)
        else:
            return error_permission_denied(command)
    
    elif command.startswith("vulnerabilities "):
        if check_permission("defender:vulnerabilities", myaccess):
            vulnerabilities_input = command[len("vulnerabilities "):].strip()
            return run_vulnerabilities_command(vulnerabilities_input)
        else:
            return error_permission_denied(command)
        
    elif command.startswith("endpoint "):
        if check_permission("defender:endpoint", myaccess):
            endpoint_input = command[len("endpoint "):].strip()
            return run_endpoint_command(endpoint_input)
        else:
            return error_permission_denied(command)
    
    else:
        return error_unknown_command(command, "defender")