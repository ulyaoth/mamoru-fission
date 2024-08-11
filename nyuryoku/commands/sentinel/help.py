# commands/sentinel/help.py

def get_sentinel_help_menu():
    return (
        "Here are the Sentinel commands you can use:\n\n"
        "Sentinel Commands:\n"
        "- `sentinel help`: Display this help menu\n"
        "- `sentinel incidents open`: Shows the count of open incidents with severity breakdown in the last 30 days\n"
        "- `sentinel incidents closed`: Shows the count of closed incidents with severity breakdown in the last 30 days\n"
        "- `sentinel incidents summary`: Provides a summary of open and closed incidents in the last 30 days\n"
        "- `sentinel incidents trending`: Displays incident trends over the past 4 weeks with severity breakdown\n\n"
        "If you have any questions, please reach out to us."
    )
