# commands/user/myinfo.py

def get_user_myinfo_menu(myaccess: str, user_realname: str) -> str:
    return (
        "Thank you for using Mamoru your security assistant and more!\n\n"
        "Your Info:\n"
        f" `Name`: {user_realname}\n"
        f" `Access Level`: {myaccess}\n\n"
        "If you have any questions, please reach out to us."
    )
