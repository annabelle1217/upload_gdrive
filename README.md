# Google Drive Uploader

A python scripts that uses Google Drive API to upload folders or files.

## Installation 
1. Git clone this repo:
```
git clone https://github.com/Techyhans/upload_gdrive
```
2. Create a virtual environment:
```
conda create -n gdrive-api
```
3. Install required dependencies:
```
conda install pip
pip install PyDrive
```

## Download using Google Drive API
You need to state two arguments to run [upload.py](upload.py).
- '-f' or '--folder': Files or folders path to be uploaded (Must have at least one).
- '-i' or '--id': The folder ID to upload files or folders to (Must have only one).

For example:
- To upload a folder with all items it contains:
```
python upload_gdrive.py -f sample -i 1n_xfeDvSzcakM565oHBq_BOOXJL4hWiY
```

- To upload multiple folders or files:
```
python upload_gdrive.py -f sample/folder_1 sample/folder_2 sample.jfif -i 1n_xfeDvSzcakM565oHBq_BOOXJL4hWiY
```

Take note: Remember to change the id to the folder ID in your Google Drive. Also, if you have not create your client_secret.json, follow the steps on my medium [Google Drive API Authentication](https://hansheng0512.medium.com/download-folders-and-files-using-google-drive-api-and-python-1ad086e769b#:~:text=SECTION%201%3A%20AUTHENTICATION) (this step allows Google Drive API to access resource on your Google Drive).