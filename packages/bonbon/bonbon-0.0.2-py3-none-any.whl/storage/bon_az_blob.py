import json
from azure.storage import CloudStorageAccount


def azure_blob_get(account_name, account_key,
                   container_name, blob_name):
    """Return json format."""
    account = CloudStorageAccount(account_name, account_key)
    blockblob_service = account.create_block_blob_service()
    blob_object = blockblob_service.get_blob_to_text(container_name, blob_name)
    return json.loads(blob_object.content)


def azure_blob_upload(account_name, account_key,
                      container_name, blob_name, file_path):
    """Upload file (path) to blob."""
    account = CloudStorageAccount(account_name, account_key)
    blockblob_service = account.create_block_blob_service()
    blockblob_service.create_container(container_name)
    blockblob_service.create_blob_from_path(
        container_name, blob_name, file_path)


if __name__ == "__main__":
    print('### bon azure blob ###')
