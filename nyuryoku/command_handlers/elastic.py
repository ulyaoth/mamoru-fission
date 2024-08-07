# command_handlers/elastic.py

from commands.elastic.help import get_elastic_help_menu
from error_handler.error import error_unknown_elastic_command

def run_elastic_command(command: str) -> str:
    if command == "help":
        return get_elastic_help_menu()
    else:
        return error_unknown_elastic_command(command)