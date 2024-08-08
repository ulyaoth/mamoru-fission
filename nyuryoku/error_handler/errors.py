# error_handler/errors.py

def error_unknown_command(command: str, context: str) -> str:
    if context == "common":
        return (
            f"*Error*\n\n*{command}* is not a valid input.\n"
            "Please see /mamoru help for a list of acceptable commands."
        )
    else:
        return (
            f"*Error*\n\n*{command}* is not a valid input for {context}.\n"
            "Please see /mamoru {context} help for a list of acceptable commands."
        )

def error_invalid_cve_format(command: str) -> str:
    return (
        f"*Error*\n\n*{command}* is not a valid CVE format.\n"
        "The correct format for a CVE is 'CVE-YYYY-NNNN' (e.g., CVE-2021-34527).\n"
        "Please see /mamoru help for a list of acceptable commands."
    )