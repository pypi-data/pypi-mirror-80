from os import path, listdir
from pathlib import Path
import shutil
from typing import List, Mapping

try:
    from sh import mount, umount
except:
    def mount(path: str):
        pass

    def umount(path: str):
        pass

from teslacam.config import Configuration
from teslacam.consts import TESLACAM_DIR, RECENT_DIR, SAVED_DIR, SENTRY_DIR
from teslacam.enums import ClipType
from teslacam.models import Clip

CLIP_TYPE_DIR_MAPPING: Mapping[ClipType, str] = {
    ClipType.RECENT: RECENT_DIR,
    ClipType.SAVED: SAVED_DIR,
    ClipType.SENTRY: SENTRY_DIR
}

class FileSystem:
    def __init__(self, cfg: Configuration):
        self.__cfg = cfg

    def read_clips(self, type: ClipType) -> List[Clip]:
        clips_dir = path.join(self.__cfg.tesla_cam_directory,
            TESLACAM_DIR, CLIP_TYPE_DIR_MAPPING[type])

        clips_path = Path(clips_dir)

        if not clips_path.exists():
            return []

        clips = FileSystem.__get_items(clips_path, type)

        return clips

    def delete_empty_event_dirs(self, type: ClipType):
        clips_dir = path.join(self.__cfg.tesla_cam_directory,
            TESLACAM_DIR, CLIP_TYPE_DIR_MAPPING[type])

        clips_path = Path(clips_dir)

        if not clips_path.exists():
            return

        for dir in [item for item in clips_path.iterdir() if item.is_dir()]:
            items = [item for item in listdir(dir) if not item.startswith(".")]
            
            if len(items) == 0:
                shutil.rmtree(dir)

    def mount_directory(self):
        try:
            mount(self.__cfg.tesla_cam_directory)
        except:
            return

    def unmount_directory(self):
        try:
            umount(self.__cfg.tesla_cam_directory)
        except:
            return

    @staticmethod
    def __get_items(clips_path: Path, type: ClipType, items: List[Clip]=None, event: str=None) -> List[Clip]:
        items = [] if items == None else items

        for item in clips_path.iterdir():
            if item.is_file() and path.splitext(item.name)[1] == ".mp4":
                try:
                    clip = Clip(item, type, event)
                    items.append(clip)
                except ValueError:
                    continue

            elif item.is_dir():
                FileSystem.__get_items(item, type, items, item.name)

        return items