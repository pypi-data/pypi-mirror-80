from typing import Mapping, Type

from teslacam.contracts import Notifier, Uploader
from teslacam.notifiers.pushover import PushoverNotifier
from teslacam.uploaders.blobstorage import BlobStorageUploader
from teslacam.uploaders.filesystem import FileSystemUploader

UPLOADERS: Mapping[str, Type[Uploader]] = {
    "blobStorage": BlobStorageUploader,
    "fileSystem": FileSystemUploader
}

NOTIFIERS: Mapping[str, Type[Notifier]] = {
    "pushover": PushoverNotifier
}

TESLACAM_DIR = "TeslaCam"
RECENT_DIR = "RecentClips"
SAVED_DIR = "SavedClips"
SENTRY_DIR = "SentryClips"

ONE_MEGABYTE = 1048576

MIN_FILE_SIZE_BYTES = ONE_MEGABYTE # 1 MB