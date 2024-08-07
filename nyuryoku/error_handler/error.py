# error_handler/errors.py

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
