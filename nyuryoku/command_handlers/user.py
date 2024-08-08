# command_handlers/tenable.py

from commands.user.help import get_user_help_menu
from nyuryoku.error_handler.errors import error_unknown_command

def run_user_command(command: str) -> str:
    if command == "help":
        return get_user_help_menu()
    else:
        return error_unknown_command(command, "user")