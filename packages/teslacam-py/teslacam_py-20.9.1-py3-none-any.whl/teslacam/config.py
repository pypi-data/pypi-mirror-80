from os import path
from typing import Any, List, Optional

import yaml

from teslacam.enums import ClipType

CONFIG_PATH = "/etc/teslacam.yml"

class Configuration:
    def __init__(self, cfg: dict):
        self.__cfg = cfg

        self.__set_required_config()
        self.__set_optional_config()

    def __set_required_config(self):
        self.__tesla_cam_directory = self.__cfg["teslaCamDirectory"]
        self.__mount_directory = self.__cfg["mountDirectory"]
        self.__clip_types = [ClipType[type] for type in self.__cfg["clipTypes"]]

    def __set_optional_config(self):
        self.__uploader = self.__cfg.get("uploader")
        self.__notifier = self.__cfg.get("notifier")
        self.__upload_interval = self.__cfg.get("uploadInterval") or 30
        self.__last_event_clips_count = self.__cfg["lastEventClipsCount"] or 10

    def __getitem__(self, key: str) -> Any:
        return self.__cfg[key]

    @property
    def tesla_cam_directory(self) -> str:
        """
        Directory containing the TeslaCam directory.
        """
        return self.__tesla_cam_directory

    @property
    def mount_directory(self) -> bool:
        """
        Indicates whether the tesla_cam_directory should be mounted.
        """
        return self.__mount_directory

    @property
    def last_event_clips_count(self) -> int:
        """
        The amount of latest clips that should be uploaded for every event.
        """
        return self.__last_event_clips_count

    @property
    def uploader(self) -> Optional[str]:
        """
        The uploader to use.
        """
        return self.__uploader

    @property
    def clip_types(self) -> List[ClipType]:
        """
        Which clip types to upload.
        """
        return self.__clip_types

    @property
    def notifier(self) -> Optional[str]:
        """
        The notifier to use.
        """
        return self.__notifier

    @property
    def upload_interval(self) -> int:
        """
        The delay between upload job starts.
        """
        return self.__upload_interval

def load_config() -> Configuration:
    """
    Loads the application configuration from config.yml.
    """
    cfg_path = CONFIG_PATH if path.isfile(CONFIG_PATH) else "config.yml"

    with open(cfg_path) as file:
        cfg = yaml.load(file, Loader=yaml.FullLoader)
        return Configuration(cfg)