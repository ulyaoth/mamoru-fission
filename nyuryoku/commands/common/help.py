# commands/common/help.py

from command_handlers.command_registry import command_registry  # Lazy import to avoid circular dependency
from role_handlers.role_registry import check_permission

def get_slack_help_menu(myaccess: str) -> str:
    # Start building the help menu
    help_menu = "Thank you for using Mamoru, your security assistant and more!\n\n"
    help_menu += "Here are the commands you can use:\n"

    # Always include common commands that are permitted for the user
    help_menu += "Common:\n"
    if check_permission("common:help", myaccess):
        help_menu += "- `help`: Display this help menu\n"
    if check_permission("common:version", myaccess):
        help_menu += "- `version`: Who doesn't love a version number\n"

    # Dynamically add sections for each command in the registry based on the user's permissions
    for command_prefix in command_registry:
        if command_prefix == "common":  # Skip "common" since it's already handled
            continue

        # Check if the user has any permissions related to the command prefix
        if any(check_permission(f"{command_prefix}:{cmd}", myaccess) for cmd in ["help"]):
            help_menu += f"{command_prefix.capitalize()} Commands:\n"
            if check_permission(f"{command_prefix}:help", myaccess):
                help_menu += f"- `{command_prefix} help`: Show the available commands for {command_prefix.capitalize()}\n"

    help_menu += "\nIf you have any questions, please reach out to us."

    return help_menu

def get_teams_help_menu():
    return (
        "Thank you for using Mamoru your security assistant!\n"
        "Here are the commands you can use:\n"
        "- `help`: Display this help menu\n"
        "If you have any questions, please reach out to us."
    )
