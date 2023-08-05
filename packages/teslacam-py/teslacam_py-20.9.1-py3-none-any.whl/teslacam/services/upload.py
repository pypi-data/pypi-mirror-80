from datetime import datetime
from threading import Timer
from typing import List, Optional, Tuple

from teslacam.config import Configuration
from teslacam.consts import MIN_FILE_SIZE_BYTES, ONE_MEGABYTE, UPLOADERS
from teslacam.enums import ClipType
from teslacam.funcs import group_by
from teslacam.log import log
from teslacam.models import Clip
from teslacam.services.filesystem import FileSystem
from teslacam.services.notification import NotificationService

class UploadService:
    def __init__(self, cfg: Configuration, fs: FileSystem, notification: NotificationService):
        self.__cfg = cfg
        self.__fs = fs
        self.__notification = notification

        if cfg.uploader:
            self.__uploader = UPLOADERS[cfg.uploader](cfg)

        self.__timer: Optional[Timer] = None

    def start(self):
        """
        Starts a timer that will periodically upload TeslaCam clips.
        """
        if self.__timer is not None:
            return

        self.__timer = Timer(self.__cfg.upload_interval, self.__process_clips)
        self.__timer.start()

    def __process_clips(self):
        try:
            if (self.__cfg.mount_directory):
                self.__fs.mount_directory()

            total_uploaded = 0

            for type in self.__cfg.clip_types:
                total_uploaded += self.__process_of_type(type)

            if (self.__cfg.mount_directory):
                self.__fs.unmount_directory()
            
            log("Processing complete")

            if total_uploaded > 0:
                self.__notification.notify(f"Uploaded {total_uploaded} new TeslaCam clips")
        except:
            log("Processing failed, retrying later")

        self.__timer = None
        self.start()

    def __process_of_type(self, type: ClipType) -> int:
        log(f"Processing {str(type)} clips...")

        clips = self.__fs.read_clips(type)
        log(f"Found {len(clips)} clips")

        uploaded = 0

        (to_upload, to_delete) = self.__get_clips_to_upload(clips)

        for i, clip in enumerate(to_upload, start=1):
            log(f"Uploading clip '{clip.name}' ({format_size(clip)}) ({i}/{len(to_upload)})")
                
            if self.__uploader is not None and self.__uploader.upload(clip):
                clip.delete()
                uploaded += 1

        for clip in to_delete:
            log(f"Deleting clip '{clip.name}' ({format_size(clip)})")
            clip.delete()

        self.__fs.delete_empty_event_dirs(type)

        return uploaded

    def __get_clips_to_upload(self, clips: List[Clip]) -> Tuple[List[Clip], List[Clip]]:
        """
        Gets a tuple with the clips to upload and the clips to delete.
        """
        to_upload: List[Clip] = []
        to_skip: List[Clip] = []

        for event, event_clips in group_by(clips, lambda c: c.event).items():
            # Events less than 3 minutes ago will be skipped over for now
            if event is not None:
                diff = (datetime.today() - event).total_seconds() / 60

                if diff < 3.0:
                    to_skip.extend(event_clips)
                    break

            clips_by_date = group_by(event_clips, lambda c: c.date)
            dates = sorted(clips_by_date.keys())[-self.__cfg.last_event_clips_count:]

            clips_to_upload = [clip
                for date in dates
                for clip in clips_by_date[date]
                if clip.size >= MIN_FILE_SIZE_BYTES]

            to_upload.extend(clips_to_upload)

        to_delete = [clip
            for clip in clips
            if clip not in to_upload
            and clip not in to_skip]

        log(f"Will upload {len(to_upload)}, skip {len(to_skip)} and delete {len(to_delete)}")

        return (to_upload, to_delete)

def format_size(clip: Clip) -> str:
    return f"{round(clip.size / ONE_MEGABYTE, 2)} MB"