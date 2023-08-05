from teslacam.config import Configuration
from teslacam.consts import NOTIFIERS

class NotificationService:
    def __init__(self, cfg: Configuration):
        if cfg.notifier:
            self.__notifier = NOTIFIERS[cfg.notifier](cfg)

    def notify(self, msg: str):
        if not self.__notifier:
            return

        try:
            self.__notifier.notify(msg)
        except:
            return