"""
Spam be gone!
"""


import src.slack as slack


def clear_channel(channel_name: str="nolava"):
    """
    Clear the nolava channel.
    """
    bot = slack.user_by_name("deepthought")
    channel = slack.channel_by_name(channel_name)
    history = slack.chat_history(channel)

    deepthought_messages = [
        msg for msg in history
        if msg.user == bot
    ]

    for message in deepthought_messages:
        slack.delete_message(message)


if __name__ == "__main__":
    clear_channel()
