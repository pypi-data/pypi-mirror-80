from chump import Application

from teslacam.config import Configuration
from teslacam.contracts import Notifier

PUSHOVER_CONFIG_KEY = "pushoverNotifier"

class PushoverNotifier(Notifier):
    def __init__(self, cfg: Configuration):
        super().__init__(cfg)

        pushover_cfg = cfg[PUSHOVER_CONFIG_KEY]
        apiToken = pushover_cfg["apiToken"]
        userKey = pushover_cfg["userKey"]

        application = Application(apiToken)
        self.__user = application.get_user(userKey)

    def notify(self, message: str):
        self.__user.send_message(message)