# commands/common/help.py

def get_slack_help_menu():
    return (
        "Thank you for using Mamoru your security assistant and more!\n\n"
        "Here are the commands you can use:\n"
        "Common:\n"
        "- `help`: Display this help menu\n"
        "- `version`: Who doesn't love a version number\n"        
        "Sentinel Commands:\n"
        "- `sentinel help`: Show the available commands for Sentinel\n"
        "Elastic Commands:\n"
        "- `elastic help`: Show the available commands for Elastic\n"
        "Tenable Commands:\n"
        "- `tanable help`: Show the available commands for tenable\n"
        "Defender Commands:\n"
        "- `defender help`: Show the available commands for defender\n"
        "User Commands:\n"
        "- `user help`: Show user specific commands\n\n"
        "If you have any questions, please reach out to us."
    )

def get_teams_help_menu():
    return (
        "Thank you for using Mamoru your security assistant!\n"
        "Here are the commands you can use:\n"
        "- `help`: Display this help menu\n"
        "If you have any questions, please reach out to us."
    )
