# File Sync Project

This project includes three Python scripts for automatic file synchronization from a local folder to a remote backup server.

## Methods Implemented

- `sync_scp.py`: Uses SCP for simple file transfer
- `sync_sftp.py`: Uses SFTP with Paramiko and SSH key
- `sync_rsync.py`: Uses rsync for efficient syncing of new/changed files

All scripts use `watchdog` to monitor the folder and trigger transfers automatically.
