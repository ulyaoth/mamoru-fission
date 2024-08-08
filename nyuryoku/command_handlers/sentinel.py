# command_handlers/sentinel.py

from commands.sentinel.help import get_sentinel_help_menu
from error_handler.errors import error_unknown_command

def run_sentinel_command(command: str) -> str:
    if command == "help":
        return get_sentinel_help_menu()
    else:
        return error_unknown_command(command, "sentinel")