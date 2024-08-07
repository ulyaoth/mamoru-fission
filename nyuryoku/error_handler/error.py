# error_handler/error.py

def error_slack_unknown_command(command: str) -> str:
    return (
        f"*Error*\n\n*{command}* is not a valid input.\n"
        "Please see /mamoru help for a list of acceptable commands."
     )

def error_unknown_sentinel_command(command: str) -> str:
    return (
        f"*Error*\n\n*{command}* is not a valid input for sentinel.\n"
        "Please see /mamoru help for a list of acceptable commands."
     )

def error_unknown_elastic_command(command: str) -> str:
    return (
        f"*Error*\n\n*{command}* is not a valid input for elastic.\n"
        "Please see /mamoru help for a list of acceptable commands."
     )

def error_unknown_defender_command(command: str) -> str:
    return (
        f"*Error*\n\n*{command}* is not a valid input for defender.\n"
        "Please see /mamoru help for a list of acceptable commands."
     )

def error_unknown_tenable_command(command: str) -> str:
    return (
        f"*Error*\n\n*{command}* is not a valid input for tenable.\n"
        "Please see /mamoru help for a list of acceptable commands."
     )