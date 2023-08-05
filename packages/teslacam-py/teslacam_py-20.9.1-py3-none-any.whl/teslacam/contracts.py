from abc import ABC, abstractmethod

from teslacam.config import Configuration
from teslacam.models import Clip

class Notifier(ABC):
    def __init__(self, cfg: Configuration):
        pass

    @abstractmethod
    def notify(self, message: str):
        pass

class Uploader(ABC):
    def __init__(self, cfg: Configuration):
        pass

    @abstractmethod
    def upload(self, clip: Clip) -> bool:
        """
        Uploads the clip.
        """
        pass