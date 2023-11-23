from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os
import glob

# Google drive api auth
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

# The variable we specify
directory_path = '/home/pi/Pictures'
folder_id = '1GXcT1o8iFkjG6WV53lY_lk-Fu32pvFQ7'

# To check the file is exist or not
def find_latest_jpg(path):
    jpg_files = glob.glob(os.path.join(path, '*.jpg'))
    # If there is not a JPG image, it will stop
    if not jpg_files:
        print(f"No JPG files found in {path}")
        return None
    latest_png = max(jpg_files, key=os.path.getmtime)
    # Return the path 
    return latest_png

# Call the function to find and print the latest JPG file
latest_image_path = find_latest_jpg(directory_path)
if latest_image_path:
    print(f"Latest image file: {latest_image_path}")
    f = drive.CreateFile({
        'title': os.path.basename(latest_image_path),
        'mimeType': 'image/jpeg', 
        'parents': [{'kind': 'drive#fileLink', 'id': folder_id}]
    })
    f.SetContentFile(latest_image_path)
    f.Upload()
    print("File uploaded to Google Drive.")
else:
    print("No image file found.")

