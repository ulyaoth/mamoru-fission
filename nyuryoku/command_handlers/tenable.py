# command_handlers/tenable.py

from commands.tenable.help import get_tenable_help_menu
from error_handler.errors import error_unknown_command, error_permission_denied
from role_handlers.role_registry import check_permission

def run_tenable_command(command: str, myaccess: str) -> str:
    if command == "help":
        if check_permission("tenable:help", myaccess):
            return get_tenable_help_menu()
        else:
            return error_permission_denied(command)
    
    else:
        return error_unknown_command(command, "tenable")
