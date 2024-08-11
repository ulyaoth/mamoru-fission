# command_handlers/sentinel.py

from commands.sentinel.help import get_sentinel_help_menu
from commands.sentinel.incidents import run_sentinel_incidents_command
from error_handler.errors import error_unknown_command, error_permission_denied
from role_handlers.role_registry import check_permission

def run_sentinel_command(command: str, myaccess: str) -> str:
    if command == "help":
        if check_permission("sentinel:help", myaccess):
            return get_sentinel_help_menu()
        else:
            return error_permission_denied(command)
        
    elif command.startswith("incidents "):
        if check_permission("defender:incidents", myaccess):
            incidents_input = command[len("incidents "):].strip()
            return run_sentinel_incidents_command(incidents_input)
        else:
            return error_permission_denied(command)
    
    else:
        return error_unknown_command(command, "sentinel")
