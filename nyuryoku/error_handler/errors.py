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
            f"Please see /mamoru {context} help for a list of acceptable commands."
        )

def error_invalid_cve_format(command: str, context: str) -> str:
    return (
        f"*Error*\n\n*{command}* is not a valid CVE format.\n"
        "The correct format for a CVE is 'CVE-YYYY-NNNN' (e.g., CVE-2021-34527).\n"
        f"Please see /mamoru {context} help for a list of acceptable commands."
    )

def error_invalid_vulnerabilities_input(command: str, context: str) -> str:
    return (
        f"*Error*\n\n*{command}* is not a valid input for {context} vulnerabilities.\n"
        "Please specify 'low', 'medium', 'high', or 'total'.\n"
        f"Please see /mamoru {context} help for a list of acceptable commands."
    )

def error_permission_denied(command: str) -> str:
    return (
        f"*Access Denied*\n\nYou do not have the necessary permissions to execute the *{command}* command.\n"
        "Please contact your system administrator if you believe this is an error.\n"
        "You can see the list of available commands for your role using `/mamoru help`."
    )

def error_invalid_ip_input(ip_input: str) -> str:
    return (
        f"*Invalid IP Address*\n\nThe IP address *{ip_input}* is not valid.\n"
        "Please enter a valid IPv4 or IPv6 address and try again.\n"
        "If you need help with the command syntax, you can use `/mamoru help`."
    )
