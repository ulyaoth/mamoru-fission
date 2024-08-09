# commands/common/version.py

def get_version():
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": (
                    "Thank you for using Mamoru, your security assistant and more!\n\n"
                    "*Name:* Mamoru\n"
                    "*Version:* 0.1\n"
                    "*GitHub:* <https://github.com/ulyaoth/mamoru-fission>\n\n"
                    "If you have any questions, please reach out to us."
                ),
            },
        },
        {
            "type": "image",
            "image_url": "https://raw.githubusercontent.com/ulyaoth/mamoru-fission/main/slack-bot-image-512x512.png",
            "alt_text": "Mamoru Logo",
        },
    ]
