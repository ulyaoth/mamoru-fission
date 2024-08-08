# command_handlers/user.py

from commands.user.help import get_user_help_menu
from commands.user.myinfo import get_user_myinfo_menu
from error_handler.errors import error_unknown_command

def run_user_command(command: str) -> str:
    if command == "help":
        return get_user_help_menu()
    elif command == "myinfo":
        return get_user_myinfo_menu()
    else:
        return error_unknown_command(command, "user")