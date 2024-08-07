# commands/common/help.py

def get_slack_help_menu():
    return (
        "Thank you for using Mamoru your security assistant and more!\n\n"
        "Here are the commands you can use:\n"
        "Common:\n"
        "- `help`: Display this help menu\n"
        "- `ip <address>`: Check details for an IP address (IPv4 or IPv6)\n"
        "- `sha <hash>`: Check details for a SHA hash (SHA-1 or SHA-256)\n"
        "- `cve <cve-number>`: Check details for a CVE number (format: CVE-XXXX-XXXX)\n\n"
        "Sentinel Commands:\n"
        "- `sentinel help`: Show the available commands for Sentinel\n"
        "Elastic Commands:\n"
        "- `elastic help`: Show the available commands for Elastic\n"
        "Tenable Commands:\n"
        "- `tanable help`: Show the available commands for tenable\n"
        "Defender Commands:\n"
        "- `defender help`: Show the available commands for defender\n\n"
        "If you have any questions, please reach out to us."
    )

def get_teams_help_menu():
    return (
        "Thank you for using Mamoru your security assistant!\n"
        "Here are the commands you can use:\n"
        "- `help`: Display this help menu\n"
        "If you have any questions, please reach out to us."
    )
