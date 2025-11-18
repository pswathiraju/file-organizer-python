import os
import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCH_FOLDER = r"c:\Users\ADMIN\Downloads"   

FILE_TYPES = {
    "Images": [".png", ".jpg", ".jpeg", ".gif"],
    "Documents": [".pdf", ".docx", ".txt"],
    "Videos": [".mp4", ".mov", ".avi"],
    "Compressed": [".zip", ".rar"],
    "Music": [".mp3", ".wav"],
    "Others": []
}

def create_folders():
    for folder in FILE_TYPES:
        path = os.path.join(WATCH_FOLDER, folder)
        if not os.path.exists(path):
            os.makedirs(path)

def move_file(file_path):
    time.sleep(1)  

    if not os.path.exists(file_path):
        print("File disappeared:", file_path)
        return

    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    # Find matching folder
    for folder, extensions in FILE_TYPES.items():
        if ext in extensions:
            dest = os.path.join(WATCH_FOLDER, folder, os.path.basename(file_path))
            shutil.move(file_path, dest)
            print(f"MOVED → {dest}")
            return

    # Default → Others
    dest = os.path.join(WATCH_FOLDER, "Others", os.path.basename(file_path))
    shutil.move(file_path, dest)
    print(f"MOVED → {dest}")

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print("Detected new file:", event.src_path)
            move_file(event.src_path)

if __name__ == "__main__":
    print("STARTING WATCHER...")
    print("Watching:", WATCH_FOLDER)
    create_folders()

    observer = Observer()
    observer.schedule(Handler(), WATCH_FOLDER, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
