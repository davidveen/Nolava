"""
Gets the next message from stack (if any), and takes appropriate follow-up
actions.
"""
import threading
import src.slack as slack
import typing


class WorkerThread(threading.Thread):
    """
    Worker thread for getting messages from the database and posting thse to
    Slack.
    """
    def __init__(self):
        super().__init__()
        # self._nolava_id = slack.channel_by_name("nolava").id

    def run(self):
        pass

    def post_message(self) -> None:
        """
        Post message to slack
        """
        pass

    def mark_message_posted(self):
        """
        Mark message as posted.
        """
        pass

    def get_message(self) -> typing.Optional[typing.Tuple[str, str]]:
        """
        Get the next message from queue.

        Returns message and recipient. Returns `None` when no messages are
        available.
        """
        pass
