# commands/common/help.py

def get_slack_help_menu():
    return (
        "Thank you for using Mamoru your security assistant!\n\n"
        "Here are the commands you can use:\n"
        "Common:\n"
        "- `help`: Display this help menu\n"
        "- `ip <address>`: Check details for an IP address (IPv4 or IPv6)\n"
        "- `sha <hash>`: Check details for a SHA hash (SHA-1 or SHA-256)\n"
        "- `cve <cve-number>`: Check details for a CVE number (format: CVE-XXXX-XXXX)\n\n"
        "Sentinel Commands:\n"
        "- `sentinel <parameter>`: Check sentinel data for given parameter\n"
        "Elastic Commands:\n"
        "- `test`: test\n\n"
        "Endpoint Commands:\n"
        "- `sentinel <parameter>`: Check sentinel data for given parameter\n\n"
        "If you have any questions, please reach out to us."
    )

def get_teams_help_menu():
    return (
        "Thank you for using Mamoru your security assistant!\n"
        "Here are the commands you can use:\n"
        "- `help`: Display this help menu\n"
        "If you have any questions, please reach out to us."
    )
