"""
Gets the next message from stack (if any), and takes appropriate follow-up
actions.
"""
import threading
import typing

import src.data_access as db
import src.slack as slack


class WorkerThread(threading.Thread):
    """
    Worker thread for getting messages from the database and posting these to
    Slack.

    Worker thread is started as daemonic on instantiation.

    Usage:
    >>> src.worker_thread.WorkerThread()
    """

    _select_message = (
        "SELECT id, recipient_id, payload "
        "FROM MessageQueue "
        "WHERE processed=0;"
    )

    _mark_posted = (
        "UPDATE MessageQueue "
        "SET processed=1 "
        "WHERE id={id};"
    )

    def __init__(self):
        # Start as daemonic so this thread will not prevent Python from
        # closing
        super().__init__(daemon=True)
        self.start()

    def run(self):
        while self._main():
            pass

    def _main(self) -> bool:
        for msg in self._get_message():
            message_id, recipient_id, message = msg.values()
            self._post_message(message, recipient_id)
            self._mark_message_posted(message_id)
            # NOTE TODO Please create a quit-message to nicely terminate this
            #           thread.
            # if message == message_quit:
                # return False
        return True

    def _post_message(self, message: str, recipient_id: str) -> None:
        """
        Post message to slack
        """
        slack.post_message(recipient_id, message)

    def _mark_message_posted(self, message_id: int) -> None:
        """
        Mark message as posted.
        """
        db.query(self._mark_posted.format(id=message_id))

    def _get_message(self) -> typing.Tuple[int, str, str]:
        """
        Get the next message from queue.

        Returns message-id, message and recipient. Returns `None` when no
        messages are available.
        """
        queue = db.query(self._select_message)
        for message in queue:
            yield message

    def _create_test_queue(self, user):
        db.query(
            "INSERT INTO MessageQueue (recipient_id, payload, processed) "
            f"VALUES ('{user}', 'this is a message coming from the db', 0);"
        )
