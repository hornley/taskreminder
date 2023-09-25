from datetime import datetime, date
import os
import shutil
from pathlib import Path

path = Path(__file__).parents[2]


if "Log" not in os.listdir(path):
    os.mkdir(f"{path}Log")
if "Changes" not in os.listdir(f"{path}\Log"):
    os.mkdir(f"{path}\Log\Changes")
if "Backup" not in os.listdir(path):
    os.mkdir(f"{path}\Backup")

changes_log = fr"{path}\Log\Changes\\"
backup_path = fr"{path}\Backup"
tasks_path = fr"{path}\Tasks.txt"

def getTime():
    time_now = datetime.now()
    date_now = date.today()
    current_time = time_now.strftime("%H:%M:%S")

    time = f"{date_now} {current_time}"
    time = time.replace(":", "-")
    return time

def changes():
    time = getTime()
    if time[:10] not in os.listdir(changes_log):
        os.mkdir(changes_log + "\\" + fr"{time[:10]}")
    path = open(fr"{changes_log}{time[:10]}\{time[:10]}.txt", "a")
    path.close()
    return path

def backup():  # boa
    time = getTime()
    if time[:10] not in os.listdir(backup_path):
        os.mkdir(backup_path + "\\" + fr"{time[:10]}")
    file_name = f"Backup-{time}"
    shutil.copy(tasks_path, fr"{backup_path}\{time[:10]}\{file_name}.txt")