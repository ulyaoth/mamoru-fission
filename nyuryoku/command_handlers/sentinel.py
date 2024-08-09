# command_handlers/sentinel.py

from commands.sentinel.help import get_sentinel_help_menu
from error_handler.errors import error_unknown_command, error_permission_denied
from role_handlers.role_registry import check_permission

def run_sentinel_command(command: str, myaccess: str) -> str:
    if command == "help":
        if check_permission("sentinel:help", myaccess):
            return get_sentinel_help_menu()
        else:
            return error_permission_denied(command)
    
    else:
        return error_unknown_command(command, "sentinel")
