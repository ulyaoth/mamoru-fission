# command_handlers/tenable.py

from commands.tenable.help import get_tenable_help_menu
from error_handler.error import error_unknown_tenable_command

def run_tenable_command(command: str) -> str:
    if command == "help":
        return get_tenable_help_menu()
    else:
        return error_unknown_tenable_command(command)