from azure.storage.blob import BlobServiceClient
from backend.core.config import Config

blob_service_client = BlobServiceClient.from_connection_string(Config.BLOB_CONNECTION_STRING)

def list_blob_files():
    """List all files in the Azure Blob Storage container."""
    container_client = blob_service_client.get_container_client(Config.BLOB_CONTAINER_NAME)
    return [blob.name for blob in container_client.list_blobs()]
