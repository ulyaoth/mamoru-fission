# command_handlers/tenable.py

from commands.tenable.help import get_tenable_help_menu
from nyuryoku.error_handler.errors import error_unknown_command

def run_tenable_command(command: str) -> str:
    if command == "help":
        return get_tenable_help_menu()
    else:
        return error_unknown_command(command, "tenable")