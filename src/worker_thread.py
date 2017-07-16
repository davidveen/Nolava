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

    def _main(self):
        msg = self._get_message()
        if msg:
            message_id, message, recipient_id = msg
            self._post_message(message, recipient_id)
            self._mark_message_posted(message_id)

    def _post_message(self, message: str, recipient_id: str) -> None:
        """
        Post message to slack
        """
        slack.post_message(recipient_id, message)

    def _mark_message_posted(self, message_id: int) -> None:
        """
        Mark message as posted.
        """
        pass

    def _get_message(self) -> typing.Optional[typing.Tuple[int, str, str]]:
        """
        Get the next message from queue.

        Returns message-id, message and recipient. Returns `None` when no
        messages are available.
        """
        pass
