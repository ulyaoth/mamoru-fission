# command_handlers/user.py

from commands.user.help import get_user_help_menu
from commands.user.myinfo import get_user_myinfo_menu
from error_handler.errors import error_unknown_command, error_permission_denied
from role_handlers.role_registry import check_permission

def run_user_command(command: str, myaccess: str, user_realname: str) -> str:
    if command == "help":
        if check_permission("user:help", myaccess):
            return get_user_help_menu()
        else:
            return error_permission_denied(command)
    
    elif command == "myinfo":
        if check_permission("user:myinfo", myaccess):
            return get_user_myinfo_menu(myaccess, user_realname)
        else:
            return error_permission_denied(command)
    
    else:
        return error_unknown_command(command, "user")
