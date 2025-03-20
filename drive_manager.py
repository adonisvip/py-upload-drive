import os
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io

# def get_drive_structure(service, parent_id=None):
#     query = f"'{parent_id}' in parents" if parent_id else "'root' in parents"
#     results = service.files().list(q=query, fields="files(id, name, mimeType, parents)").execute()
#     return results.get("files", [])

def get_drive_structure(service, parent_id=None):
    query = f"'{parent_id}' in parents and trashed=false" if parent_id else "'root' in parents and trashed=false"
    results = service.files().list(q=query, fields="files(id, name, mimeType, parents)").execute()
    return results.get("files", [])

def create_folder(service, folder_name, parent_id=None):
    folder_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
    }
    if parent_id:
        folder_metadata["parents"] = [parent_id]

    folder = service.files().create(body=folder_metadata, fields="id").execute()
    return folder["id"]

def upload_file(service, file_path, parent_id=None):
    file_name = os.path.basename(file_path)
    file_metadata = {"name": file_name}
    if parent_id:
        file_metadata["parents"] = [parent_id]

    media = MediaFileUpload(file_path, resumable=True)
    service.files().create(body=file_metadata, media_body=media).execute()

def download_file(service, file_id, file_name, save_path):
    request = service.files().get_media(fileId=file_id)
    with io.FileIO(save_path, "wb") as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
