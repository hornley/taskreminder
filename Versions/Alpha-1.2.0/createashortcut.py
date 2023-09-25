import os, win32com.client
from pathlib import Path

def create():
    path1 = Path(__file__).parents[2]

    path = os.path.join(path1, 'TaskReminder - Shortcut.lnk')
    target = fr"{path1}\dist\TaskReminder\TaskReminder.exe"
    icon = fr"{path1}\dist\TaskReminder\TaskReminder.exe"

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = target
    shortcut.IconLocation = icon
    shortcut.save()