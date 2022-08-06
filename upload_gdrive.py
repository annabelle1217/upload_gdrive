import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import argparse


def onerror(func, path, exc_info):
    # Is the error an access error?
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise


def connect_google_drive_api():
    """
    Initialise connection to Gdrive API to access Google Drive
    """
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("mycreds.txt")

    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds and save
        gauth.Authorize()
    gauth.SaveCredentialsFile("mycreds.txt")

    drive = GoogleDrive(gauth)

    return drive


def get_children(drive, root_folder_id):
    """
    List all folders/files under a parent folder
    """
    str = "'" + root_folder_id + "'" + " in parents and trashed=false"
    file_list = drive.ListFile({"q": str}).GetList()
    return file_list


def get_folder_id(drive, root_folder_id, root_folder_title):
    """
    Find a child folder id given the folder name 
    and parent folder id
    """
    file_list = get_children(drive, root_folder_id)
    for file in file_list:
        if file["title"] == root_folder_title:
            return file["id"]


def upload_gdrive_file(drive, name, path, folder_id):
    """
    Upload files onto google drive
    """
    f = drive.CreateFile({"title": name, "parents": [{"id": folder_id}]})
    f.SetContentFile(path)
    f.Upload()


def upload_gdrive_folder(drive, folder_path, id):
    """
    Upload folders onto google drive
    """
    folder_name = os.path.basename(folder_path)
    folder = drive.CreateFile(
        {
            "title": folder_name,
            "parents": [{"id": id}],
            "mimeType": "application/vnd.google-apps.folder",
        }
    )
    folder.Upload()

    folder_id = get_folder_id(drive, id, folder_name)
    print(f"Create {folder_name} {folder_id}.")

    for name in os.listdir(folder_path):
        path = os.path.join(folder_path, name)
        if os.path.isdir(path):
            upload_gdrive_folder(drive, path, folder_id)
        else:
            print(f"    Uploading {path}")
            upload_gdrive_file(drive, name, path, folder_id)


def main(drive, folder, root_id):
    for folder in opt.folder:
        if os.path.isdir(folder):
            upload_gdrive_folder(drive, folder, root_id)
        else:
            print(f"Uploading {folder}")
            upload_gdrive_file(drive, folder, folder, root_id)
    print("All Done!")

def parse_opt():
    parser = argparse.ArgumentParser()   
    parser.add_argument(
        "-f",
        "--folder",
        type=str,
        nargs="+",
        help="Files or folders path to be uploaded (Must have at least one).",
    )
    parser.add_argument(
        "-i",
        "--id",
        type=str,
        nargs=1,
        help="The folder ID to upload files or folders to (Must have only one).",
    )
    opt = parser.parse_args()
    return opt


if __name__ == "__main__":
    opt = parse_opt()
    drive = connect_google_drive_api()
    main(drive, opt.folder, opt.id[0])
