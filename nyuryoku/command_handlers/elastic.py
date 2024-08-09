# command_handlers/elastic.py

from commands.elastic.help import get_elastic_help_menu
from error_handler.errors import error_unknown_command, error_permission_denied
from role_handlers.role_registry import check_permission

def run_elastic_command(command: str, myaccess: str) -> str:
    if command == "help":
        if check_permission("elastic:help", myaccess):
            return get_elastic_help_menu()
        else:
            return error_permission_denied(command)
    
    else:
        return error_unknown_command(command, "elastic")
