# -----------------------------------------------
# File Sync Script using rsync
# This script monitors a folder and syncs new files efficiently using rsync over SSH.
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
            print(f"New file detected: {event.src_path}")
            self.transfer_file()

    def transfer_file(self):
        try:
            rsync_command = [
                "rsync",
                "-avz",
                "--ignore-existing",
                f"{SOURCE_DIR}/",
                f"{USERNAME}@{BACKUP_SERVER}:{REMOTE_DIR}/"
            ]
            subprocess.run(rsync_command, check=True)
            print("Transfer completed using rsync.")
        except subprocess.CalledProcessError as e:
            print(f"Transfer error with rsync: {e}")

if __name__ == "__main__":
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, SOURCE_DIR, recursive=False)
    observer.start()
    print(f"Monitoring folder: {SOURCE_DIR}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
