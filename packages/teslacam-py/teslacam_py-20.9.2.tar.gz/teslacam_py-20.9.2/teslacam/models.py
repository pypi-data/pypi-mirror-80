from datetime import datetime
from pathlib import Path
import re
from typing import Optional

from teslacam.enums import ClipType, Camera

DATE_REGEX = re.compile(r"^(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})-")
CAMERA_REGEX = re.compile(r"-(\w+)\.mp4")

DATE_FORMAT = r"%Y-%m-%d_%H-%M-%S"

CAMERA_DICT = {
    "front": Camera.FRONT,
    "left_repeater": Camera.LEFT_REPEATER,
    "right_repeater": Camera.RIGHT_REPEATER,
    "back": Camera.BACK
}

class Clip:
    def __init__(self, path: Path, type: ClipType, event: str=None):
        self.__pathObject = path

        self.__path = str(path)
        self.__name = path.name
        self.__type = type
        self.__size = path.stat().st_size

        self.__event = datetime.strptime(event, DATE_FORMAT) if event is not None else None

        date = DATE_REGEX.findall(self.name)[0]
        self.__date = datetime.strptime(date, DATE_FORMAT)

        camera = CAMERA_REGEX.findall(self.name)[0]
        self.__camera = CAMERA_DICT[camera]

    @property
    def path(self) -> str:
        """
        Path to the clip file on the file system.
        """
        return self.__path

    @property
    def name(self) -> str:
        """
        Name of the clip.
        """
        return self.__name

    @property
    def type(self) -> ClipType:
        """
        Type of the clip.
        """
        return self.__type

    @property
    def date(self) -> datetime:
        """
        Date the clip was created.
        """
        return self.__date

    @property
    def camera(self) -> Camera:
        """
        Camera the clip was recorded with.
        """
        return self.__camera

    @property
    def event(self) -> Optional[datetime]:
        """
        Event (save/sentry) this clip is a part of.
        """
        return self.__event

    @property
    def size(self) -> int:
        """
        Size of the clip in bytes.
        """
        return self.__size

    def delete(self):
        """
        Deletes a clip from disk.
        """
        self.__pathObject.unlink()