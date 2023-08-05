from azure.storage.blob import ContainerClient, BlobClient
from azure.core.exceptions import ResourceNotFoundError, ServiceRequestError

from teslacam.config import Configuration
from teslacam.contracts import Uploader
from teslacam.models import Clip

BLOB_STORAGE_CONFIG_KEY = "blobStorageUploader"

class BlobStorageUploader(Uploader):
    def __init__(self, cfg: Configuration):
        super().__init__(cfg)

        blob_cfg = cfg[BLOB_STORAGE_CONFIG_KEY]
        account_name = blob_cfg["accountName"]
        account_key = blob_cfg["accountKey"]
        container_name = blob_cfg["containerName"]

        self.__container_client = ContainerClient(f"https://{account_name}.blob.core.windows.net/",
            container_name, account_key, retry_total=1, connection_timeout=5)

    def upload(self, clip: Clip) -> bool:
        dir = f"{clip.date.year}/{clip.date.month}/{clip.date.day}" if clip.event != None else "recent"
        blob_name = f"{dir}/{clip.name}"

        blob = self.__container_client.get_blob_client(blob_name)

        try:
            blob.get_blob_properties()
            return True
        except ResourceNotFoundError:
            return self.__perform_upload(clip, blob)
        except ServiceRequestError:
            return False

    def __perform_upload(self, clip: Clip, blob: BlobClient) -> bool:
        try:
            with open(clip.path, "rb") as data:
                blob.upload_blob(data)
            return True
        except:
            return False