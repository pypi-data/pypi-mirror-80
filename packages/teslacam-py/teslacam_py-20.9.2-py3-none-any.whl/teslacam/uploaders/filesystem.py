from teslacam.models import Clip
from teslacam.contracts import Uploader

class FileSystemUploader(Uploader):
    def upload(self, clip: Clip) -> bool:
        return True