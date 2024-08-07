# command_handlers/elastic.py

from error_handler.error import error_elastic_unknown_command

def run_elastic_command(command: str) -> str:
        return error_elastic_unknown_command(command)