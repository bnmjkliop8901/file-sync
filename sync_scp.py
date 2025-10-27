# -----------------------------------------------
# File Sync Script using SCP
# This script monitors a folder and transfers new files to a backup server using SCP.
# -----------------------------------------------


import time
import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

SOURCE_DIR = "/home/soheil/WatchFolder"
BACKUP_SERVER = "10.35.210.39"
USERNAME = "backupuser"
REMOTE_DIR = "/home/backupuser/backup"

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f" New file detected: {event.src_path}")
            self.transfer_file(event.src_path)

    def transfer_file(self, filepath):
        filename = os.path.basename(filepath)
        remote_path = f"{USERNAME}@{BACKUP_SERVER}:{REMOTE_DIR}/{filename}"
        try:
            subprocess.run(["scp", filepath, remote_path], check=True)
            print(f" Transfer completed: {filename}")
        except subprocess.CalledProcessError as e:
            print(f" Transfer error with scp: {e}")

if __name__ == "__main__":
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, SOURCE_DIR, recursive=False)
    observer.start()
    print(f" Monitoring: {SOURCE_DIR}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

