# import time
# import os
# import subprocess
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler

# SOURCE_DIR = "/home/soheil/WatchFolder"
# BACKUP_SERVER = "10.35.210.39"
# USERNAME = "backupuser"
# REMOTE_DIR = "/home/backupuser/backup"

# class FileHandler(FileSystemEventHandler):
#     def on_created(self, event):
#         if not event.is_directory:
#             print(f" New file detected: {event.src_path}")
#             self.transfer_file(event.src_path)

#     def transfer_file(self, filepath):
#         filename = os.path.basename(filepath)
#         remote_path = f"{USERNAME}@{BACKUP_SERVER}:{REMOTE_DIR}/{filename}"
#         try:
#             subprocess.run(["scp", filepath, remote_path], check=True)
#             print(f" Transfer completed: {filename}")
#         except subprocess.CalledProcessError as e:
#             print(f" Transfer error with scp: {e}")

# if __name__ == "__main__":
#     event_handler = FileHandler()
#     observer = Observer()
#     observer.schedule(event_handler, SOURCE_DIR, recursive=False)
#     observer.start()
#     print(f" Monitoring: {SOURCE_DIR}")
#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         observer.stop()
#     observer.join()







# import time
# import os
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
# import paramiko


# SOURCE_DIR = "/home/soheil/WatchFolder"
# BACKUP_SERVER = "10.35.210.39"
# USERNAME = "backupuser"
# REMOTE_DIR = "/home/backupuser/backup"
# KEY_PATH = "/home/soheil/.ssh/id_rsa"

# class FileHandler(FileSystemEventHandler):
#     def on_created(self, event):
#         if not event.is_directory:
#             print(f"New file detected: {event.src_path}")
#             self.transfer_file(event.src_path)

#     def transfer_file(self, filepath):
#         filename = os.path.basename(filepath)
#         try:
#             key = paramiko.RSAKey.from_private_key_file(KEY_PATH)
#             transport = paramiko.Transport((BACKUP_SERVER, 22))
#             transport.connect(username=USERNAME, pkey=key)
#             sftp = paramiko.SFTPClient.from_transport(transport)
#             sftp.put(filepath, f"{REMOTE_DIR}/{filename}")
#             sftp.close()
#             transport.close()
#             print(f"Transfer completed: {filename}")
#         except Exception as e:
#             print(f"Transfer error with SFTP: {e}")

# if __name__ == "__main__":
#     event_handler = FileHandler()
#     observer = Observer()
#     observer.schedule(event_handler, SOURCE_DIR, recursive=False)
#     observer.start()
#     print(f"Monitoring: {SOURCE_DIR}")
#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         observer.stop()
#     observer.join()









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
