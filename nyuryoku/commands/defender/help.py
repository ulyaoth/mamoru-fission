# commands/defender/help.py

def get_defender_help_menu():
    return (
        "Here are the Defender commands you can use:\n\n"
        "Defender Commands:\n"
        "- `defender help`: Display this help menu\n"
        "- `defender check-cve <cve-number>`: Checks if a CVE is found in Defender (format: CVE-XXXX-XXXX)\n"
        "- `defender vulnerabilities <low|medium|high|total>`: Shows vulnerabilities based on severity or total vulnerabilities\n"
        "- `defender endpoint mostvln`: Shows the most vulnerable endpoint and last login details\n"
        "- `defender endpoint <device-name>`: Shows vulnerability summary for a specific device\n\n"
        "If you have any questions, please reach out to us."
    )

