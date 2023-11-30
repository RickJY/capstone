from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os
import glob
import time

# Google drive api auth
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

# The variable we specify
directory_path = '/home/pi/Pictures'
folder_id = '1GXcT1o8iFkjG6WV53lY_lk-Fu32pvFQ7'

# To check if there is a new file
def find_latest_jpg(path, last_checked_time):
    jpg_files = glob.glob(os.path.join(path, '*.jpg'))

    # If there are no JPG files, it will stop
    if not jpg_files:
        print(f"No JPG files found in {path}")
        return None, last_checked_time

    # Find the latest file based on modification time
    latest_jpg = max(jpg_files, key=os.path.getmtime)
    latest_mtime = os.path.getmtime(latest_jpg)

    # Check if the latest file is newer than the last checked time
    if latest_mtime > last_checked_time:
        print(f"New image file found: {os.path.basename(latest_jpg)}")
        return latest_jpg, latest_mtime
    else:
        print("No new image files.")
        return None, last_checked_time

# Initialize the last checked time with the current time
last_checked_time = time.time()

# Periodically check for new files (adjust the sleep duration as needed)
while True:
    latest_image_path, last_checked_time = find_latest_jpg(directory_path, last_checked_time)
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
        os.system('python3 AWS_connect.py')
    # Adjust the sleep duration based on your desired frequency of checking for new files
    time.sleep(10)  # Sleep for 60 seconds before checking again
